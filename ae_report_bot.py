#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
#sys.path.append(r'/Users/haohe/Python/spider/aeGame/')
import os
import time
import re
from qqbot import qqbotsched

#2378314127
log_path = '/root/aeBot/moving_fleets_report.txt'

def prepareData():
	with open(log_path,'r') as f:
		result = f.readlines()
		if(result[-1] == 'done\n'):
			return ''.join(result)
		else:
			result = 'result is not ready, please wait...'
	return result

@qqbotsched(hour='0-23',minute='0-59/10')
def autoReport(bot):
	group = bot.List('group','Astro Empire T服群')[0]
	if (group is None):
		return
	if (not os.path.isfile(log_path)):
		pass
	else:
		report = prepareData()
		if (report[0][0]!='[' ):
			print('nothing to report...')
			pass
		else:
			bot.SendTo(group,'警告: 发现偷鸡部队, 请使用 -报告 查看')

def onQQMessage(bot,contact,member,content):
	if bot.isMe(contact,member):
		print('自言自语...')
	else:
		if content == '-报告':
			if (not os.path.isfile(log_path)):
					bot.SendTo(contact,'偷鸡报告未生成, 请等待...')
			else:
				report = prepareData()
				bot.SendTo(contact,report)
				#os.remove('/Users/haohe/Desktop/moving_fleets_report.txt')
		elif content == '-hello':
			bot.SendTo(contact,'我是谁,我在哪,我要干嘛...')
		elif '@ME' in content:
			outData = member.name+', 明天就去你家偷鸡'
			bot.SendTo(contact,outData)
		elif content == '-stop-':
			bot.SendTo(contact,'emergency shuting down....please check...')
			bot.Stop()
		elif content == '-版本':
			outData = '当前版本为 偷鸡雷达v0.3测试版\n1. 每隔5分钟自动搜索T2x星系的偷鸡舰队\n'
			outData = outData + '2. 可在qq群通过偷鸡机器人查看相关报告\n'
			outData = outData + '3. 每10分钟检查一次是否有偷鸡舰队，自动触发报警\n'
			bot.SendTo(contact,outData)
		elif content == '-帮助':
			outData = '目前支持的指令有: \n-报告 用于查看已生成的偷鸡报告\n-hello 调戏机器人\n'
			outData = outData + '-版本 显示当前偷鸡雷达版本及功能'
			bot.SendTo(contact, outData)
	time.sleep(3)



#time.sleep() to lock frequent reply
#sched to generate report

'''or
during scan mode, open a thread/await to get report from ae server
a) block IO, put qqbot to sleep (question: how many seconds? will need to make a pool, and wakeup 
once complete)
b) non-block... qqbot is ready to do other request...

once a report is generated, in ?mins cannot scan again
hint user that wants to scan to look at report first
'''

