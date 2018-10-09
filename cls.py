import random
import asyncio
import time
from datetime import datetime
import sched
import event


class Send:  # メッセージ送信用クラス
	@staticmethod
	def send(msg, client, loop, reply=None):
		if reply is None:
			reply = msg.content
		asyncio.ensure_future(client.send_message(msg.channel, reply), loop=loop)


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


class Reminder:  # リマインダー用クラス
	@staticmethod
	def remind(msg, client, loop):
		run_at = msg.content[8:18]
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
		msg.content = msg.content[19:]
		if msg.content == '':
			msg.content = msg.author.mention + ' リマインダーです'
		else:
			msg.content = msg.author.mention + ' ' + msg.content
		scheduler = sched.scheduler(time.time, time.sleep)
		scheduler.enterabs(run_at, 1, Send.send, argument=(msg, client, loop))
		asyncio.async(client.send_message(msg.channel, 'リマインダーを設定しました。'), loop=loop)
		scheduler.run()


class Event:  # イベントスケジューラ用クラス
	@staticmethod
	def remind(msg, client, loop):
		global event_schedule
		time_now = datetime.now()
		event_scheduler = sched.scheduler(time.time, time.sleep)
		event_type = msg.content[7:10]
		if event_type == 'dlf':
			event_schedule = event.dlf(msg.content)
		elif event_type == 'tbs':
			event_schedule = event.tbs(msg.content)
		if event_schedule is False:
			asyncio.async(client.send_message(msg.channel, '入力形式が間違っています。 /event dlf 180731 のように入力してください。'), loop=loop)
			return 0
		for remind_time, remind_msg in event_schedule.items():
			if remind_time > int(time.mktime(time_now.utctimetuple())):
				event_scheduler.enterabs(remind_time, 1, Send.send, argument=(msg, client, loop, remind_msg))
		asyncio.async(client.send_message(msg.channel, 'イベントスケジュールを正常に読み込みました。'), loop=loop)
		event_scheduler.run()
