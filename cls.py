import random


class Tachibana:  # 橘です！用クラス
	val = False
	reply_list = ['橘です。', '橘です！', '名前で呼ばないでください！', '......ありすでいいです']

	def __init__(self):
		pass

	@classmethod
	def toggle(cls):
		cls.val is not cls.val

	@classmethod
	def reply(cls):
		return random.choice(cls.reply_list)
