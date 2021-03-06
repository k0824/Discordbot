import random
import asyncio
import time
from datetime import datetime
import sqlite3
import sched
import event
import idolinfo
import threading


def gen_id():
    return int(time.mktime(datetime.now().utctimetuple())) % 100000


# メッセージ送信用関数
def send(msg, channel, client, loop):
    return asyncio.ensure_future(client.send_message(channel, msg), loop=loop)


class DataBase:  # データベース用クラス
    db_name = 'database.db'

    @classmethod
    def insert(cls, _id, _time, msg, table, guild, channel_id, *args):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        if table == 'reminders':
            reply_at, author = map(str, args)
            c.execute('insert into reminders values(?, ?, ?, ?, ?, ?, ?)', (str(_id), str(_time), str(msg), str(author), str(reply_at), str(guild), str(channel_id)))
        elif table == 'event_schedules':
            round_num = list(map(str, args))[0]
            c.execute('insert into event_schedules values(?, ?, ?, ?, ?, ?)', (str(_id), str(_time), str(msg), str(guild), str(channel_id), str(round_num)))
        conn.commit()

    # データベースに登録されているリマインダー・イベント情報を返す
    @classmethod
    def info(cls, _guild):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        ret = '現在設定されているリマインダー一覧:\n'
        reminder_list = list(map(str, c.execute('select ID, time, message, author, guild from reminders')))
        for item in reminder_list:
            _id, _time, msg, author, guild = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            if guild == _guild:
                _time = '20{0}/{1}/{2} {3}:{4}'.format(_time[0:2], _time[2:4], _time[4:6], _time[6:8], _time[8:])
                ret += 'ID : {0} | 設定者 : {1} | {2} {3}\n'.format(_id, author, _time, msg)
        ret += '現在設定されているイベント一覧:\n'
        event_list = list(map(str, c.execute('select ID, start_day, event_type, guild from event_schedules')))
        for item in event_list:
            _id, _time, _type, guild = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            if _type == 'dlf':
                _type = 'ドリームLIVEフェスティバル'
            elif _type == 'tbs':
                _type = 'トークバトルショー'
            elif _type == 'pdc':
                _type = 'ぷちデレラコレクション'
            elif _type == 'ltc':
                _type = 'LIVEツアーカーニバル'
            elif _type == 'idc':
                _type = 'アイドルチャレンジ'
            if guild == _guild:
                _time = '20{0}/{1}/{2}'.format(_time[0:2], _time[2:4], _time[4:6])
                ret += 'ID : {0} | {1} 開始 {2}\n'.format(_id, _time, _type)
        return ret

    @classmethod
    def delete(cls, table, _id):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        c.execute('delete from {0} where ID = {1}'.format(table, _id))
        conn.commit()
        return '{0} テーブルから ID:{1} のレコードを削除しました。'.format(table, _id)

    # 起動時にデータベースを参考にしてリマインダーとイベントを復元する
    @classmethod
    def on_boot(cls, client, loop):
        # コネクトオブジェクト生成
        conn = sqlite3.connect(cls.db_name)
        # カーソル生成
        c = conn.cursor()
        # リマインダーの復元
        reminder_list = list(map(str, c.execute('select ID, time, message, author, guild, channel, reply_at from reminders')))
        for item in reminder_list:
            _id, _time, msg, author, guild, channel, reply_at = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            remind = Remind(guild, channel, client, _time, loop, msg, reply_at, author, _id=_id, insert_flag=False)
            remind_thread = threading.Thread(target=remind.set)
            remind_thread.start()
        # イベントの復元
        event_list = list(map(str, c.execute('select ID, start_day, event_type, guild, channel, round_num from event_schedules')))
        for item in event_list:
            _id, _time, _type, guild, channel, round_num = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            event = Event(guild, channel, client, _time, loop, _type, int(round_num), _id=_id, insert_flag=False)
            event_thread = threading.Thread(target=event.set)
            event_thread.start()


# sched関連クラス
class Schedule:
    # 全てのイベントをIDと紐づけて管理する辞書
    event_dict = {}
    # イベントを管理するスケジューラ
    scheduler = sched.scheduler(time.time, time.sleep)
    
    # 初期化 insert_flag はそれがチャットで呼び出されたものなのかを判定するbool
    # guild : msg.guild.id
    # time : msg.content.split()[2]
    # channel : msg.channel
    def __init__(self, guild, channel_id, client, time, loop, _id=1000000, insert_flag=True):
        self.guild = guild
        self.channel_id = channel_id
        self.channel = client.get_channel(channel_id)
        self.client = client
        self.loop = loop
        self.insert_flag = insert_flag
        self.time = time
        if _id == 1000000:
            self.id = gen_id()
        else:
            self.id = _id


class Remind(Schedule):
    # リマインダー時のみ利用する変数の初期化
    # msg = msg.content.split()[3] OR 'リマインダーです。'
    # reply_at = msg.author.mention
    # author = msg.author.display_name
    def __init__(self, guild, channel, client, time, loop, msg, reply_at, author, _id=1000000, insert_flag=True):
        super().__init__(guild, channel, client, time, loop, _id, insert_flag)
        self.msg = ' '.join(msg)
        self.reply_at = reply_at
        self.author = author
        self.table = 'reminders'
    
    # リマインダー設定関数
    def set(self):
        # run_at_datetime を作成、失敗したらエラーメッセージを発言
        try:
            run_at_datetime = datetime.strptime('20'+self.time, '%Y%m%d%H%M')
        except:
            asyncio.async(self.client.send_message(self.channel, '入力形式が間違っています。2018/7/31 20:30 にリマインダーを設定したい場合は、 /sched remind 1807312030 [リマインド時に送信する文言] のように入力してください。'), loop=self.loop)
            return None
        # 設定時刻が過去のもの、かつinsert_flagがTrueのときにエラーメッセージを発言
        if run_at_datetime < datetime.now() and self.insert_flag:
            asyncio.async(self.client.send_message(self.channel, '入力した日時が過去のものです。'), loop=self.loop)
            return None
        # run_at_datetime から絶対時刻 run_at_at に変換
        run_at_at = int(time.mktime(run_at_datetime.utctimetuple()))
        # insert_flag が True ならデータベースにリマインダー情報を登録
        if self.insert_flag:
            DataBase.insert(self.id, self.time, self.msg, self.table, self.guild, self.channel_id, self.reply_at, self.author)
        # Event を scheduler に登録、Event情報をIDと紐づけて辞書 super().event_dict に保管
        super().event_dict[self.id] = super().scheduler.enterabs(run_at_at, 1, send, argument=('{0} : {1}'.format(self.reply_at, self.msg), self.channel, self.client, self.loop))
        # 正常にリマインド出来たらキャンセル関数を走らせる
        super().scheduler.enterabs(run_at_at+1, 1, Remind.cancel, argument=(self.id,))
        # insert_flag が True なら設定完了発言
        if self.insert_flag:
            send('リマインダーを設定しました。', self.channel, self.client, self.loop)
        # スケジューラ開始
        super().scheduler.run()

    # リマインダーキャンセル関数
    @classmethod
    def cancel(cls, _id):
        # 親クラスの event_dict から指定したidに合致する Event を pop してキャンセル
        try:
            super().scheduler.cancel(super().event_dict.pop(_id))
        except:
            pass
        # データベースから削除
        return DataBase.delete('reminders', _id)


class Event(Schedule):
    # イベント用リマインダーのみ利用する変数の初期化
    # type : msg.content.split()[3]
    def __init__(self, guild, channel, client, time, loop, _type, round, _id=1000000, insert_flag=True):
        super().__init__(guild, channel, client, time, loop, _id, insert_flag)
        self.type = _type
        self.round = round
        self.table = 'event_schedules'

    # イベント用リマインダー設定関数
    def set(self):
        # イベントの通知を集めるリスト
        event_list = []
        # 現在時刻を取得
        time_now = datetime.now()
        # イベントタイプに応じてスケジュールを OrderedDict で取得
        event_schedule = event.switch(self.type, self.time, self.round)
        # 上の処理でエラーが起きた場合等、エラーメッセージを発言
        if event_schedule is False:
            asyncio.async(self.client.send_message(self.channel, '入力形式が間違っています。 /sched event dlf 180731 のように入力してください。'), loop=self.loop)
            return None
        # insert_flag が True ならデータベースにイベント情報を登録
        if self.insert_flag:
            DataBase.insert(self.id, self.time, self.type, self.table, self.guild, self.channel.id, self.round)
        # 取得したイベントスケジュールに対してリマインダーを一つずつ設定
        for remind_time, remind_msg in event_schedule.items():
            if remind_time > int(time.mktime(time_now.utctimetuple())):
                event_list.append(super().scheduler.enterabs(remind_time, 1, send, argument=(remind_msg, self.channel, self.client, self.loop)))
        # Event情報をIDと紐づけて辞書 super().event_dict に保管
        super().event_dict[self.id] = event_list
        # 正常にリマインド出来たらキャンセル関数を走らせる
        super().scheduler.enterabs(list(event_schedule.keys())[-1]+1, 1, Event.cancel, argument=(self.id,))
        # insert_flag が True なら設定完了発言
        if self.insert_flag:
            send('イベントを設定しました。', self.channel, self.client, self.loop)
        # スケジューラ開始
        super().scheduler.run()

    # イベント用リマインダーキャンセル関数
    @classmethod
    def cancel(cls, _id):
        # 親クラスの event_dict から指定したidに合致する Event (配列)を pop して順次キャンセル
        event_list = super().event_dict.pop(_id)
        for _event in event_list:
            try:
                super().scheduler.cancel(_event)
            except:
                pass
        # データベースから削除
        return DataBase.delete('event_schedules', _id)


class Tachibana:  # 橘です！用クラス
    val = False
    reply_list = ['橘です。', '橘です！', '名前で呼ばないでください！', '......ありすでいいです']

    def __init__(self):
        pass

    @classmethod
    def toggle(cls):
        cls.val = not cls.val

    @classmethod
    def reply(cls):
        return random.choice(cls.reply_list)


class IdolInfo:  # idolinfo用クラス
    @staticmethod
    def info(name):
        ret = ''
        __dict = idolinfo.info(name)
        for item, info in __dict.items():
            if info is not None:
                ret += '{0} : {1}   '.format(item, info)
        return ret
