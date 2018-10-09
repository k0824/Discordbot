import discord  # discord 用パッケージ
import asyncio  # asyncIO
from cls import Tachibana  # tachibana


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

	# /neko
	if message.content.startswith('/neko'):
		await client.send_message('にゃーん')

	# 'ありす' に反応
	if 'ありす' in message.content and client.user != message.outhor and Tachibana.val is True:
		await client.send_message(Tachibana.reply())
	# /tachibana によるトグル
	if message.content.startswith('/tachibana'):
		Tachibana.toggle()

# botの起動と接続
client.run(token)
