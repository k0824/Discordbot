import time
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict


# ラウンド名のリストを作成
def make_round_list(num):
    rounds = []
    for i in range(num)[0:-1]:
        rounds.append('第{0}'.format(i+1))
    rounds.append('最終')
    return rounds


def switch(event_type, first_day, round_num):
    if event_type == 'dlf':
        event_schedule = dlf(first_day, round_num)
    elif event_type == 'tbs':
        event_schedule = tbs(first_day, round_num)
    elif event_type == 'ltc':
        event_schedule = ltc(first_day, round_num)
    elif event_type == 'pdc':
        event_schedule = pdc(first_day, round_num)
    elif event_type == 'idc':
        event_schedule = idc(first_day, round_num)
    elif event_type == 'pmf':
        event_schedule = pmf(first_day)
    elif event_type == 'idr':
        event_schedule = idr(first_day, round_num)
    elif event_type == 'idp':
        event_schedule = idp(first_day, round_num)
    else:
        event_schedule = False
    return event_schedule


# ドリームLIVEフェスティバル
def dlf(first_day, round_num):
    name = 'ドリームLIVEフェスティバル'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = make_round_list(round_num)
    time_first_day = [1800, 1850, 2200, 2350, 10700, 10850, 11200, 11250, 11900, 12050]
    time_mid_day = [2200, 2350, 10700, 10850, 11200, 11250, 11900, 12050]
    time_last_day = [2200, 2350, 10700, 10850, 11200, 11250, 11800, 11850, 12100, 12250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        elif round == round_num - 1:
            timetable = time_last_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # first_day との差delta の設定
            delta = timedelta(days=round)
            if times >= 10000:
                delta += timedelta(days=1)
                time_ = times - 10000
            else:
                delta = delta
                time_ = times
            delta += timedelta(seconds=((time_ - time_ % 100) / 100 * 60 + (time_ % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if times == timetable[0]:
                dic[remind_time] = '{0} {1}ラウンド及びFEVERタイム開始です'.format(name, rounds[round])
            elif times == timetable[-1]:
                dic[remind_time] = '{0} {1}ラウンド終了10分前です'.format(name, rounds[round])
            else:
                if timetable.index(times) % 2 == 0:
                    dic[remind_time] = '{0} FEVERタイム開始です'.format(name)
                else:
                    dic[remind_time] = '{0} FEVERタイム終了10分前です'.format(name)
    return dic


# トークバトルショー
def tbs(first_day, round_num):
    name = 'トークバトルショー'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = make_round_list(round_num)
    time_first_day = [1500, 1800, 1850, 1900, 2200, 2250]
    time_mid_day = [700, 1200, 1250, 1300, 1800, 1850, 1900, 2200, 2250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # ブロック数の初期化
        block = 0
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # ブロック数に関して
            if timetable.index(times) % 3 == 0:
                block += 1
            # first_day との差delta の設定
            delta = timedelta(days=round, seconds=((times - times % 100) / 100 * 60 + (times % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if timetable.index(times) % 3 == 0:
                dic[remind_time] = '{0} {1}ラウンド 第{2}ブロック 開始です。'.format(name, rounds[round], str(block))
            elif timetable.index(times) % 3 == 1:
                dic[remind_time] = '{0} {1}ラウンド 第{2}ブロック ゴールデンタイム開始です。'.format(name, rounds[round], str(block))
            else:
                dic[remind_time] = '{0} {1}ラウンド 第{2}ブロック 終了10分前です。'.format(name, rounds[round], str(block))
    return dic


# LIVEツアーカーニバル
def ltc(first_day, round_num):
    name = 'LIVEツアーカーニバル'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = make_round_list(round_num)
    time_first_day = [1500, 12030, 12050]
    time_mid_day = [2200, 12030, 12050]
    time_last_day = [2200, 12230, 12250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        elif round == round_num - 1:
            timetable = time_last_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # first_day との差delta の設定
            delta = timedelta(days=round)
            if times >= 10000:
                delta += timedelta(days=1)
                time_ = times - 10000
            else:
                delta = delta
                time_ = times
            delta += timedelta(seconds=((time_ - time_ % 100) / 100 * 60 + (time_ % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if timetable.index(times) % 3 == 0:
                dic[remind_time] = '{0} {1}ラウンド 開始です。'.format(name, rounds[round])
            elif timetable.index(times) % 3 == 1:
                dic[remind_time] = '{0} {1}ラウンド 終了30分前です。'.format(name, rounds[round])
            else:
                dic[remind_time] = '{0} {1}ラウンド 終了10分前です。'.format(name, rounds[round])
    return dic


# ぷちデレラコレクション
def pdc(first_day, round_num):
    name = 'ぷちデレラコレクション'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = make_round_list(round_num)
    time_first_day = [1500, 1550, 1900, 1950, 2100, 2250]
    time_mid_day = [1200, 1250, 1900, 1950, 2100, 2250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # ステージ数の初期化
        stage = 0
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # ステージ数に関して
            stage += (timetable.index(times) + 1) % 2
            # first_day との差delta の設定
            delta = timedelta(days=round, seconds=((times - times % 100) / 100 * 60 + (times % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if timetable.index(times) % 2 == 0:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド 第' + str(stage) + 'ステージ 開始です。'
            else:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド 第' + str(stage) + 'ステージ 終了10分前です。'
    return dic


# アイドルチャレンジ
def idc(first_day, round_num):
    name = 'アイドルチャレンジ'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = make_round_list(round_num)
    time_first_day = [1500, 12030, 12050]
    time_mid_day = [2200, 12030, 12050]
    time_last_day = [2200, 12230, 12250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        elif round == round_num - 1:
            timetable = time_last_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # first_day との差delta の設定
            delta = timedelta(days=round)
            if times >= 10000:
                delta += timedelta(days=1)
                time_ = times - 10000
            else:
                delta = delta
                time_ = times
            delta += timedelta(seconds=((time_ - time_ % 100) / 100 * 60 + (time_ % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if timetable.index(times) % 3 == 0:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド開始です。'
            elif timetable.index(times) % 3 == 1:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド終了30分前です。'
            elif timetable.index(times) % 3 == 2:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド終了10分前です。'
    return dic


# プロダクションマッチフェスティバル
def pmf(first_day):
    name = 'プロダクションマッチフェスティバル'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # タイムスケジュール
    timetable = [1500, 1630, 1650, 2000, 2130, 2150,
                 11200, 11230, 11250, 11700, 11830, 11850, 12100, 12230, 12250,
                 21200, 21230, 21250, 21700, 21830, 21850, 22100, 22230, 22250,
                 31200, 31230, 31250, 31700, 31830, 31850, 32100, 32230, 32250,
                 42000, 42230, 42250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # timetable に沿ってスケジュールを設定
    for i, times in enumerate(timetable):
        # first_day との差delta の設定
        delta = timedelta()
        while times >= 10000:
            delta += timedelta(days=1)
            times = times - 10000
        delta += timedelta(seconds=((times - times % 100) / 100 * 60 + (times % 100)) * 60)
        # remind_time の設定
        try:
            remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
        except:
            return False
        remind_time = int(time.mktime(remind_time.utctimetuple()))
        if i // 3 + 1 != 12:
            battle = '第{0}'.format(i // 3 + 1)
        else:
            battle = '最終'
        if i % 3 == 0:
            dic[remind_time] = '{0} {1}戦開始です'.format(name, battle)
        elif i % 3 == 1:
            dic[remind_time] = '{0} {1}戦終了30分前です'.format(name, battle)
        elif i % 3 == 2:
            dic[remind_time] = '{0} {1}戦終了10分前です'.format(name, battle)
    return dic


# アイドルLIVEロワイヤル
def idr(first_day, round_num):
    name = 'アイドルLIVEロワイヤル'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = make_round_list(round_num)
    time_first_day = [1500, 12030, 12050]
    time_mid_day = [2200, 12030, 12050]
    time_last_day = [2200, 12230, 12250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        elif round == round_num - 1:
            timetable = time_last_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # first_day との差delta の設定
            delta = timedelta(days=round)
            if times >= 10000:
                delta += timedelta(days=1)
                time_ = times - 10000
            else:
                delta = delta
                time_ = times
            delta += timedelta(seconds=((time_ - time_ % 100) / 100 * 60 + (time_ % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if timetable.index(times) % 3 == 0:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド開始です。'
            elif timetable.index(times) % 3 == 1:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド終了30分前です。'
            elif timetable.index(times) % 3 == 2:
                dic[remind_time] = name + ' ' + rounds[round] + 'ラウンド終了10分前です。'
    return dic


# アイドルプロデュース
def idp(first_day, round_num):
    name = 'アイドルプロデュース'
    # 最後に返す辞書式配列を定義
    dic = OrderedDict()
    # ラウンドスケジュール及びタイムスケジュール
    rounds = []
    for i in range(round_num)[0:-1]:
        rounds.append('{0}日目'.format(i+1))
    rounds.append('最終日')
    time_first_day = [1500, 12030, 12050]
    time_mid_day = [2200, 12030, 12050]
    time_last_day = [2200, 12230, 12250]
    # 開始日を yymmdd の形式で取得
    first_day = '20' + first_day
    # 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
    for round in range(len(rounds)):
        # 読み込むタイムテーブルを判別
        if round == 0:
            timetable = time_first_day
        elif round == round_num - 1:
            timetable = time_last_day
        else:
            timetable = time_mid_day
        # timetable に沿ってスケジュールを設定
        for times in timetable:
            # first_day との差delta の設定
            delta = timedelta(days=round)
            if times >= 10000:
                delta += timedelta(days=1)
                time_ = times - 10000
            else:
                delta = delta
                time_ = times
            delta += timedelta(seconds=((time_ - time_ % 100) / 100 * 60 + (time_ % 100)) * 60)
            # remind_time の設定
            try:
                remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
            except:
                return False
            remind_time = int(time.mktime(remind_time.utctimetuple()))
            if timetable.index(times) % 3 == 0:
                dic[remind_time] = name + ' ' + rounds[round] + '開始です。'
            elif timetable.index(times) % 3 == 1:
                dic[remind_time] = name + ' ' + rounds[round] + '終了30分前です。'
            elif timetable.index(times) % 3 == 2:
                dic[remind_time] = name + ' ' + rounds[round] + '終了10分前です。'
    return dic
