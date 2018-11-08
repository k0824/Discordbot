"""--------------------
FlutCla's bot ver 1.1.3
レファレンス : https://hackmd.io/AZJWZiG-QxaQVn7x1eTxDA
作成 : @fl_cl_sk / @fl_cl_p
協力 : @_apple4545_
--------------------"""

import discord  # discord 用パッケージ
import asyncio  # asyncIO
import cls  # 各クラス
import threading
from data import GetToken

token = GetToken.token  # botアカウントのアクセストークン
loop = asyncio.get_event_loop()  # リマインダー用スレッドを投げるためのイベントループ取得
client = discord.Client()  # 接続用オブジェクト


# 起動時の処理
@client.event
async def on_ready():
    cls.DataBase.on_boot(client, loop)
    print('ログインが完了しました')


# メッセージ内容に応じて反応する関数
@client.event
async def on_message(message):

    # /sched 系統
    if message.content.startswith('/sched'):
        # /sched remind
        if message.content.split()[1] == 'remind':
            # 入力形式をチェックしつつ処理
            try:
                # リマインドする時間を取得
                _time = message.content.split()[2]
                # リマインド時に送信するメッセージを取得
                try:
                    msg = list(message.content.split())[3:]
                except:
                    msg = 'リマインダーです。'
                if not msg:
                    msg = 'リマインダーです。'
                # Remindクラスのオブジェクトを生成
                remind = cls.Remind(message.server.id, message.channel.id, client, _time, loop, msg, message.author.mention, message.author.display_name)
                # スレッドに投げて実行
                remind_thread = threading.Thread(target=remind.set)
                remind_thread.start()
            except:
                await client.send_message(message.channel, '正常に処理できませんでした。入力形式を確認してください。')

        # /sched event
        elif message.content.split()[1] == 'event':
            # 入力形式をチェックしつつ処理
            try:
                # イベントの開始日を取得
                _time = message.content.split()[2]
                # イベントの種類を取得
                _type = message.content.split()[3]
                # イベントのラウンド数を取得
                _round = message.content.split()[4]
                # Eventクラスのオブジェクトを生成
                event = cls.Event(message.server.id, message.channel.id, client, _time, loop, _type, _round)
                # スレッドに投げて実行
                event_thread = threading.Thread(target=event.set)
                event_thread.start()
            except:
                await client.send_message(message.channel, '正常に処理できませんでした。入力形式を確認してください。')

        # /sched info
        elif message.content.split()[1] == 'info':
            reply = cls.DataBase.info(message.server.id)
            await client.send_message(message.channel, reply)

        # /sched delete
        elif message.content.split()[1] == 'delete':
            _, _, table, _id = message.content.split()
            if table.startswith('remind'):
                reply = cls.Remind.cancel(_id)
            elif table.startswith('event'):
                reply = cls.Event.cancel(_id)
            else:
                reply = 'テーブル {0} は見つかりませんでした。'.format(table)
            await client.send_message(message.channel, reply)

    # /neko
    elif message.content.startswith('/neko'):
        await client.send_message(message.channel, 'にゃーん')

    # idolinfo
    elif message.content.startswith('/info'):
        name = list(map(str, message.content.split()))[1]
        reply = cls.IdolInfo.info(name)
        await client.send_message(message.channel, reply)

    # 'ありす' に反応
    elif 'ありす' in message.content and client.user != message.author and cls.Tachibana.val is True:
        await client.send_message(message.channel, cls.Tachibana.reply())

    # /tachibana によるトグル
    elif message.content.startswith('/tachibana'):
        cls.Tachibana.toggle()
        if cls.Tachibana.val is True:
            await client.send_message(message.channel, '橘を有効化しました')
        else:
            await client.send_message(message.channel, '橘を無効化しました')

    # /clear でログを全削除
    elif message.content.startswith('/clear'):
        await client.send_message(message.channel, 'チャンネル内のログをすべて消去します。よろしければ30秒以内に yes を送信してください')
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
