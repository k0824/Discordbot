import random
import asyncio
import time
from datetime import datetime
import sqlite3
import sched
import event
import idolinfo


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
        c.execute('insert into reminders (time, message) values (?, ?)', (_time, msg))
        conn.commit()

    @classmethod
    def insert_events(cls, start_day, event_type):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        c.execute('insert into event_schedules (start_day, event_type) values (?, ?)', (start_day, event_type))
        conn.commit()

    @classmethod
    def info_reminders(cls):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        ret = '現在設定されているリマインダー一覧です:\n'
        reminder_list = list(map(str, c.execute('select time, message from reminders')))
        for item in reminder_list:
            time1, time2, msg = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            ret += '{0} {1} : {2}\n'.format(time1, time2, msg)
        return ret

    @classmethod
    def info_events(cls):
        conn = sqlite3.connect(cls.db_name)
        c = conn.cursor()
        ret = '現在設定されているイベント一覧です:\n'
        event_schedules = list(map(str, c.execute('select start_day, event_type from event_schedules')))
        for item in event_schedules:
            _time, _type = map(str, item.replace('(', '').replace(')', '').replace("'", '').replace(',', '').split())
            if _type == 'dlf':
                _type = 'ドリームLIVEフェスティバル'
            elif _type == 'tbs':
                _type = 'トークバトルショー'
            elif _type == 'pdc':
                _type = 'ぷちデレラコレクション'
            elif _type == 'ltc':
                _type = 'LIVEツアーカーニバル'
            ret += '20{0}/{1}/{2} 開始 {3}\n'.format(_time[0]+_time[1], _time[2]+_time[3], _time[4]+_time[5], _type)
        return ret


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

    @staticmethod
    def remind(msg, client, loop, insert_flag = True):
        scheduler = sched.scheduler(time.time, time.sleep)
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
        msg.content = msg.content.split()[2]
        if msg.content == '':
            msg.content = msg.author.mention + ' リマインダーです'
        else:
            msg.content = msg.author.mention + ' ' + msg.content
        scheduler.enterabs(run_at, 1, Send.send, argument=(msg, client, loop))
        if insert_flag:
            DataBase.insert_reminders(time.strftime('%Y/%m/%d %H:%M', time.localtime(run_at)), msg.content.split()[-1])
        asyncio.async(client.send_message(msg.channel, 'リマインダーを設定しました。'), loop=loop)
        scheduler.run()


class Event:  # イベントスケジューラ用クラス
    @staticmethod
    def remind(msg, client, loop, insert_flag = True):
        global event_schedule
        time_now = datetime.now()
        event_scheduler = sched.scheduler(time.time, time.sleep)
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
            DataBase.insert_events(msg.content.split()[2], msg.content.split()[1])
        for remind_time, remind_msg in event_schedule.items():
            if remind_time > int(time.mktime(time_now.utctimetuple())):
                event_scheduler.enterabs(remind_time, 1, Send.send, argument=(msg, client, loop, remind_msg))
        asyncio.async(client.send_message(msg.channel, 'イベントスケジュールを正常に読み込みました。'), loop=loop)
        event_scheduler.run()
