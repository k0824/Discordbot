import random
import asyncio
import time
from datetime import datetime
import sqlite3
import sched
import event
import idolinfo


def gen_id():
    return int(time.mktime(datetime.now().utctimetuple())) % 10000


class Send:  # メッセージ送信用クラス
    @staticmethod
    def send(msg, client, loop, reply=None):
        if reply is None:
            reply = msg.content
        asyncio.ensure_future(client.send_message(msg.channel, reply), loop=loop)


class DataBase:  # データベース用クラス
    db_name = 'database.db'

    @classmethod
    def insert_reminders(cls, _time, msg):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        _id = gen_id()
        c.execute('insert into reminders (ID, time, message) values (?, ?, ?)', (_id, _time, msg))
        conn.commit()
        return _id

    @classmethod
    def insert_events(cls, start_day, event_type):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        _id = gen_id()
        c.execute('insert into event_schedules (ID, start_day, event_type) values (?, ?, ?)', (_id, start_day, event_type))
        conn.commit()
        return _id

    @classmethod
    def info_reminders(cls):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        ret = '現在設定されているリマインダー一覧です:\n'
        reminder_list = list(map(str, c.execute('select ID, time, message from reminders')))
        for item in reminder_list:
            _id, time1, time2, msg = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            ret += 'ID : {0} | {1} {2} : {3}\n'.format(_id, time1, time2, msg)
        return ret

    @classmethod
    def info_events(cls):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        ret = '現在設定されているイベント一覧です:\n'
        event_schedules = list(map(str, c.execute('select ID, start_day, event_type from event_schedules')))
        for item in event_schedules:
            _id, _time, _type = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            if _type == 'dlf':
                _type = 'ドリームLIVEフェスティバル'
            elif _type == 'tbs':
                _type = 'トークバトルショー'
            elif _type == 'pdc':
                _type = 'ぷちデレラコレクション'
            elif _type == 'ltc':
                _type = 'LIVEツアーカーニバル'
            ret += 'ID : {0} | 20{1}/{2}/{3} 開始 {4}\n'.format(_id, _time[0]+_time[1], _time[2]+_time[3], _time[4]+_time[5], _type)
        return ret

    @classmethod
    def delete(cls, table, _id):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        try:
            c.execute('delete from {0} where ID = {1}'.format(table, _id))
            conn.commit()
            return '{0} テーブルから ID:{1} のレコードを削除しました。'.format(table, _id)
        except:
            return '指定のテーブルにそのIDのレコードは存在しません。'


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


class Reminder:  # リマインダー用クラス
    event_dict = {}
    scheduler = sched.scheduler(time.time, time.sleep)

    @classmethod
    def remind(cls, msg, client, loop, insert_flag = True):
        run_at = msg.content.split()[1]
        run_at = '20' + run_at
        try:
            run_at = datetime.strptime(run_at, '%Y%m%d%H%M')
        except:
            reply = '入力形式が間違っています。2018/7/31 20:30 にリマインダーを設定したい場合は、 /remind 1807312030 リマインド時に送信する文言 のように入力してください。'
            asyncio.async(client.send_message(msg.channel, reply), loop=loop)
            return 0
        if run_at < datetime.now():
            asyncio.async(client.send_message(msg.channel, '入力した日時が過去のものです。'), loop=loop)
            return 0
        run_at = int(time.mktime(run_at.utctimetuple()))
        try:
            msg.content = '{0} {1}'.format(msg.author.mention, msg.content.split()[2])
        except IndexError:
            msg.content = '{0} リマインダーです'.format(msg.author.mention)
        if insert_flag:
            _id = DataBase.insert_reminders(time.strftime('%Y/%m/%d %H:%M', time.localtime(run_at)), msg.content.split()[-1])
        else:
            _id = 0
        cls.event_dict[_id] = cls.scheduler.enterabs(run_at, 1, Send.send, argument=(msg, client, loop))
        cls.scheduler.enterabs(run_at + 1, 1, cls.cancel, argument=('reminders', _id))
        asyncio.async(client.send_message(msg.channel, 'リマインダーを設定しました。'), loop=loop)
        cls.scheduler.run()

    @classmethod
    def cancel(cls, table, _id, flag = True):
        _event = cls.event_dict.pop(int(_id))
        try:
            cls.scheduler.cancel(_event)
        except:
            pass
        return DataBase.delete(table, _id)


class Event:  # イベントスケジューラ用クラス
    event_dict = {}
    event_scheduler = sched.scheduler(time.time, time.sleep)

    @classmethod
    def remind(cls, msg, client, loop, insert_flag = True):
        global event_schedule
        event_list = []
        time_now = datetime.now()
        event_type = msg.content.split()[1]
        if event_type == 'dlf':
            event_schedule = event.dlf(msg.content)
        elif event_type == 'tbs':
            event_schedule = event.tbs(msg.content)
        elif event_type == 'ltc':
            event_schedule = event.ltc(msg.content)
        else:
            event_schedule = False
        if event_schedule is False:
            asyncio.async(client.send_message(msg.channel, '入力形式が間違っています。 /event dlf 180731 のように入力してください。'), loop=loop)
            return 0
        if insert_flag:
            _id = DataBase.insert_events(msg.content.split()[2], msg.content.split()[1])
        else:
            _id = 0
        for remind_time, remind_msg in event_schedule.items():
            if remind_time > int(time.mktime(time_now.utctimetuple())):
                event_list.append(cls.event_scheduler.enterabs(remind_time, 1, Send.send, argument=(msg, client, loop, remind_msg)))
        cls.event_scheduler.enterabs(list(event_schedule.keys())[-1] + 1, 1, cls.cancel, argument=('event_schedules', _id))
        cls.event_dict[_id] = event_list
        asyncio.async(client.send_message(msg.channel, 'イベントスケジュールを正常に読み込みました。'), loop=loop)
        cls.event_scheduler.run()

    @classmethod
    def cancel(cls, table, _id):
        event_list = cls.event_dict.pop(int(_id))
        for _event in event_list:
            try:
                cls.event_scheduler.cancel(_event)
            except:
                pass
        return DataBase.delete(table, _id)
