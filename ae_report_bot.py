#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append(r'/Users/haohe/Python/spider/aeGame/')
import os
import time

#2378314127

def prepareData():
	with open('/Users/haohe/Desktop/moving_fleets_report.txt','r') as f:
		result = f.readlines()
		if(result[-1] == 'd o n e \n'):
			return '\n'.join(result)
		else:
			result = 'result is not ready, please wait...'
	return result


def onQQMessage(bot,contact,member,content):
	if bot.isMe(contact,member):
		print('自言自语...')
	else:
		if (member.name == 'dreamdragon T23' and content == '-闭嘴吧'):
			bot.SendTo(contact,'(中二)主人在叫我，程序终止...')
			bot.Stop()
		elif content == '-报告':
			if (not os.path.isfile('/Users/haohe/Desktop/moving_fleets_report.txt')):
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
		elif content == '--stop':
			bot.SendTo(contact,'emergency shuting down....please check...')
			bot.Stop()
		elif content == '-帮助':
			bot.SendTo(contact, '目前支持的指令有: ')
			bot.SendTo(contact, '-报告 用于查看已生成的偷鸡报告')
			bot.SendTo(contact, '-hello 调戏机器人')
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

