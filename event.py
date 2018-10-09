import time
from datetime import datetime
from datetime import timedelta
from collections import OrderedDict


# ドリームLIVEフェスティバル
def dlf(msg):
	dlf = 'ドリームLIVEフェスティバル'
	# 最後に返す辞書式配列を定義
	dic = OrderedDict()
	# ラウンドスケジュール及びタイムスケジュール
	rounds = ['第1', '第2', '第3', '第4', '第5', '第6', '第7', '最終']
	time_first_day = [1800, 1850, 2200, 2350, 10700, 10850, 11200, 11250, 11900, 12050]
	time_mid_day = [2200, 2350, 10700, 10850, 11200, 11250, 11900, 12050]
	time_last_day = [2200, 2350, 10700, 10850, 11200, 11250, 11800, 11850, 12100, 12250]
	# 開始日を yymmdd の形式で取得
	first_day = msg[11:17]
	first_day = '20' + first_day
	# 各ラウンドのタイムスケジュールを処理 第nラウンドはround=n-1であることに注意
	for round in range(len(rounds)):
		# 読み込むタイムテーブルを判別
		if round == 0:
			timetable = time_first_day
		elif round == 7:
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
				dic[remind_time] = dlf + ' ' + rounds[round] + 'ラウンド及びチャンスタイム開始です'
			elif times == timetable[-1]:
				dic[remind_time] = dlf + ' ' + rounds[round] + 'ラウンド終了10分前です'
			else:
				if timetable.index(times) % 2 == 1:
					dic[remind_time] = dlf + ' ' + 'FEVERタイム終了10分前です'
				else:
					dic[remind_time] = dlf + ' ' + 'FEVERタイム開始です'
	return dic


# トークバトルショー
def tbs(msg):
	tbs = 'トークバトルショー'
	# 最後に返す辞書式配列を定義
	dic = OrderedDict()
	# ラウンドスケジュール及びタイムスケジュール
	rounds = ['第1', '第2', '第3', '第4', '第5', '第6', '第7', '最終']
	time_first_day = [1500, 1850, 1900, 2250]
	time_mid_day = [700, 1250, 1300, 1850, 1900, 2250]
	# 開始日を yymmdd の形式で取得
	first_day = msg[11:17]
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
			block += (timetable.index(times) + 1) % 2
			# first_day との差delta の設定
			delta = timedelta(days=round, seconds=((times - times % 100) / 100 * 60 + (times % 100)) * 60)
			# remind_time の設定
			try:
				remind_time = datetime.strptime(first_day, '%Y%m%d') + delta
			except:
				return False
			remind_time = int(time.mktime(remind_time.utctimetuple()))
			if timetable.index(times) % 2 == 0:
				dic[remind_time] = tbs + ' ' + rounds[round] + 'ラウンド 第' + str(block) + 'ブロック 開始です。'
			else:
				dic[remind_time] = tbs + ' ' + rounds[round] + 'ラウンド 第' + str(block) + 'ブロック 終了10分前です。'
	return dic


# ぷちデレラコレクション
def pdc(msg):
	pdc = 'ぷちデレラコレクション'
	# 最後に返す辞書式配列を定義
	dic = OrderedDict()
	# ラウンドスケジュール及びタイムスケジュール
	rounds = ['第1', '第2', '第3', '第4', '第5']
	time_first_day = [1500, 1550, 1900, 1950, 2100, 2250]
	time_mid_day = [1200, 1250, 1900, 1950, 2100, 2250]
	# 開始日を yymmdd の形式で取得
	first_day = msg[11:17]
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
				dic[remind_time] = pdc + ' ' + rounds[round] + 'ラウンド 第' + str(stage) + 'ステージ 開始です。'
			else:
				dic[remind_time] = pdc + ' ' + rounds[round] + 'ラウンド 第' + str(stage) + 'ステージ 終了10分前です。'
	return dic
