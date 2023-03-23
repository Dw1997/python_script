# -*- coding: utf-8 -*-
# @Time : 2023/3/21 18:08
# @Author : wei.ding
# @Email : wei.ding@tarsocial.com
# @File : p2p2.py
# @Project : flask_test

import curses
import time
import requests
import datetime

headers = {
	'Host': 'push2.eastmoney.com',
	'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
	'Accept': 'application/json, text/plain, */*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}

secid = [
	'000821',
	'600745',
	'000762',
	'600338'
]

secids = []
for sc in secid:
	if sc.startswith('0'):
		secids.append('0.' + sc)
	elif sc.startswith('6'):
		secids.append('1.' + sc)


class ConsoleDisplay:
	def __init__(self):
		self.screen = curses.initscr()
		self.screen.border(0)
		self.running = True

	def get_values(self):
		secidstr = ','.join(secids)

		url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
		params = {
			'fltt': '2',
			'fields': 'f2,f3,f4,f12',
			'secids': secidstr
		}
		response = requests.get(url, headers=headers, params=params)
		data = response.json()
		# print(response.json())
		rows = data['data']['diff']
		return rows

	def display(self, row, col, lenth, msg):
		self.screen.addstr(row, col, " " * lenth)  # 清空该行
		self.screen.addstr(row, col, msg)
		self.screen.refresh()

	def display_list(self, row, lenth, msg_list):
		self.screen.addstr(row, 1, " " * lenth * len(msg_list))  # 清空该行
		for msg_i, msg in enumerate(msg_list):
			self.screen.addstr(row, (msg_i * lenth) + 1, msg)
		self.screen.refresh()

	def update(self):
		while self.running:
			noww = datetime.datetime.now()
			if noww.hour >= 11 and noww.minute > 30 and noww.hour < 13:
				time.sleep(5)
				continue
			try:
				rows = self.get_values()
			except:
				continue
			for row_index, row in enumerate(rows):
				now_price = row['f2']
				dp_rate = row['f3']
				dp_price = row['f4']
				secid = row['f12']
				self.display_list(row_index + 2, 14, [secid, str(now_price), str(dp_rate) + '%', str(dp_price)])
			time.sleep(0.5)

	def start(self):
		curses.noecho()
		curses.cbreak()
		self.screen.nodelay(1)

		self.screen.addstr(1, 1, " " * 14 * len(secids))  # 清空该行
		self.screen.addstr(1, 1, 'secid')
		self.screen.addstr(1, 15, 'now_price')
		self.screen.addstr(1, 29, 'dp_rate')
		self.screen.addstr(1, 43, 'dp_price')

		self.screen.refresh()
		self.update()

	def stop(self):
		self.running = False
		curses.nocbreak()
		self.screen.keypad(False)
		curses.echo()
		curses.endwin()
		print("Stopped.")


display = ConsoleDisplay()
try:
	display.start()
except KeyboardInterrupt:
	display.stop()
