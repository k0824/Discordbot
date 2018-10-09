import discord  # discord 用パッケージ
import asyncio  # asyncIO
import cls  # 各クラス
import threading

client = discord.Client()  # 接続用オブジェクト
token = 'NDk1NTU2NzExNzQ3Mjg5MDk4.DpDy1A.a1oUwLkPtvXuq72B9juG8a8TO1s'  # botアカウントのアクセストークン
loop = asyncio.get_event_loop()  # リマインダー用スレッドを投げるためのイベントループ取得


# 起動時の処理
@client.event
async def on_ready():
	print('ログインが完了しました')


# メッセージ内容に応じて反応する関数
@client.event
async def on_message(message):

	# /remind
	if message.content.startswith('/remind'):
		remind_thread = threading.Thread(target=cls.Reminder.remind, args=(message, client, loop))
		remind_thread.start()

	# /event ### YYMMDD で YYMMDD日開始の###イベントに対してリマインダーを作成
	if message.content.startswith('/event'):
		event_thread = threading.Thread(target=cls.Event.remind, args=(message, client, loop))
		event_thread.start()
		await client.send_message(message.channel, 'イベントスケジュールを読み込みます......')

	# /neko
	if message.content.startswith('/neko'):
		await client.send_message(message.channel, 'にゃーん')

	# 'ありす' に反応
	if 'ありす' in message.content and client.user != message.author and cls.Tachibana.val is True:
		await client.send_message(message.channel, cls.Tachibana.reply())
	# /tachibana によるトグル
	if message.content.startswith('/tachibana'):
		cls.Tachibana.toggle()
		if cls.Tachibana.val is True:
			await client.send_message(message.channel, '橘を有効化しました')
		else:
			await client.send_message(message.channel, '橘を無効化しました')

	# /clear でログを全削除
	if message.content.startswith('/clear'):
		await client.send_message(message.channel, 'チャンネル内のログをすべて消去します。よろしければ yes を送信してください')
		msg = await client.wait_for_message(timeout=30, author=message.author, channel=message.channel)
		if msg.content == 'yes':
			clean_flag = True
			while clean_flag is True:
				msgs = [msg async for msg in client.logs_from(message.channel)]
				if len(msgs) > 1:  # 1発言以下でdelete_messagesするとエラーになるため
					await client.delete_messages(msgs)
				else:
					clean_flag = False
					await client.send_message(message.channel, 'ログの全削除が完了しました')
		else:
			await client.send_message(message.channel, '処理を中断しました')

# botの起動と接続
client.run(token)
