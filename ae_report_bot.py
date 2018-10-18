#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#import sys
#sys.path.append(r'/Users/haohe/Python/spider/aeGame/')
import os
import time
import re
import random
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
			rand_num = random.randint(1,3)
			if (rand_num==1):
				bot.SendTo(group,'天眼通告: 客人来了, 请使用 -报告 翻牌子')
			elif (rand_num==2):
				bot.SendTo(group,'Leo大喊一声: 从来只有我吃人,居然有人来吃我，请使用 -报告 查看谁来吃Leo')
			else:
				bot.SendTo(group,'一大波僵尸来袭，勇士快来响应雅典娜的召唤，请使用 -报告 查看任务')

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
		elif content == '-roll':
			roll_num = random.randint(1,100)
			if (member.name == 'dreamdragon T23'):
				roll_num = 100
			if (roll_num < 20):
				outData = '烂人品一号登场, 偷鸡都去找你了,你的点数是: '+str(roll_num)
			elif (roll_num >= 20 and roll_num <60):
				outData = '朋友，去洗把脸吧，套套飞都比你强,你的点数是: '+str(roll_num)
			elif (roll_num >=60 and roll_num <90):
				outData = '快去偷鸡吧,这么好的运气没人抓得到你,你的点数是: '+str(roll_num)
			else:
				outData = '天选之人, 请联系管理，下次门站你的渣自动增加: '+str(roll_num*100)
			bot.SendTo(contact,outData)
		elif '@ME' in content:
			if (random.randint(1,2)==1):
				outData = member.name+', 明天就去你家偷鸡'
			else:
				outData = member.name+',我们一起分了套套飞'
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

