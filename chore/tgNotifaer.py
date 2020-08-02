import telebot
import requests
import json
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class Parser:

	def __init__(self):
		self.url = 'https://raw.githubusercontent.com/antonkurenkov/systembuilder/develop/status.json'

	def parse(self):
		return requests.get(self.url).json()


class Notifier:

	def __init__(self, raw):
		self.chat_id = 417554679 # anton
		# self.chat_id = -420442510 # ksk2020
		self.status = raw['status']
		self.bot = telebot.TeleBot(TOKEN)

	def prepare(self):
		return f'''Статус сборки: {self.status[2]["status"]}
		Версия релиза: {self.status[0]["release"]}
		Дата релиза: {self.status[1]["datetime"][:10]}'''
		

	def send(self):
		message = self.prepare()
		self.bot.send_message(self.chat_id, message, parse_mode='html')


if __name__ == "__main__":
	parser = Parser()
	status = parser.parse()
	notifier = Notifier(status)
	notifier.send()