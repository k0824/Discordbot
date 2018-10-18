import discord  # discord 用パッケージ
import asyncio  # asyncIO
import cls  # 各クラス
import threading
from data import GetToken

client = discord.Client()  # 接続用オブジェクト
token = GetToken.token  # botアカウントのアクセストークン
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

    # /sched reminder でリマインダーの設定情報を出力
    if message.content.startswith('/sched remind'):
        reply = cls.DataBase.info_reminders()
        await client.send_message(message.channel, reply)

    # /event ### YYMMDD で YYMMDD日開始の###イベントに対してリマインダーを作成
    if message.content.startswith('/event'):
        event_thread = threading.Thread(target=cls.Event.remind, args=(message, client, loop))
        event_thread.start()
        await client.send_message(message.channel, 'イベントスケジュールを読み込みます......')

    # /sched event で現在設定されているイベントスケジュールの情報を出力
    if message.content.startswith('/sched event'):
        reply = cls.DataBase.info_events()
        await client.send_message(message.channel, reply)

    # /delete table ID でテーブル内指定IDのレコードを削除
    if message.content.startswith('/delete'):
        _, table, _id = message.content.split()
        reply = ''
        if table.startswith('remind'):
            table = 'reminders'
            reply += cls.Reminder.cancel(table, _id)
        elif table.startswith('event'):
            table = 'event_schedules'
            reply += cls.Event.cancel(table, _id)
        else:
            reply += 'テーブル {0} は見つかりませんでした。'.format(table)
        await client.send_message(message.channel, reply)

    # /neko
    if message.content.startswith('/neko'):
        await client.send_message(message.channel, 'にゃーん')

    # idolinfo
    if message.content.startswith('/info'):
        name = list(map(str, message.content.split()))[1]
        reply = cls.IdolInfo.info(name)
        await client.send_message(message.channel, reply)

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
