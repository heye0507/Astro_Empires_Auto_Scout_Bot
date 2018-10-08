#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append(r'/Users/haohe/Python/spider/aeGame/')
import moving_fleets
import os

#2378314127

def prepareData():
	with open('/Users/haohe/Desktop/moving_fleets_report.txt','r') as f:
		result = f.read()
	return result

def onQQMessage(bot,contact,member,content):
	if content == '-报告':
		if (not os.path.isfile('/Users/haohe/Desktop/moving_fleets_report.txt')):
				bot.SendTo(contact,'偷鸡报告未生成, 请执行-扫描指令')
		else:
			report = prepareData()
			bot.SendTo(contact,report)
			#os.remove('/Users/haohe/Desktop/moving_fleets_report.txt')
	elif content == '-stop':
		bot.SendTo(contact,'shuting down...')
		bot.Stop()
	elif content == '-hello':
		bot.SendTo(contact,'你看我干啥...')
	elif content == '贾佳':
		bot.SendTo(contact,'老板你好,老板你今天很漂亮...')
	'''elif content == '-扫描':
		bot.SendTo(contact,'开始扫描,等待时间会比较长,完成之前机器人不响应...')
		moving_fleets.main()
		bot.SendTo(contact,'扫描完成,请使用-report指令查看报告...')'''
	elif content == '-帮助':
		bot.SendTo(contact, '目前支持的指令有: ')
		bot.SendTo(contact, '-report 用于查看已生成的偷鸡报告')
		bot.SendTo(contact, '-扫描 用于生成偷鸡报告（生产新报告视服务器情况需等待10-60秒)')
		bot.SendTo(contact, '-hello 调戏机器人')
		bot.SendTo(contact, '-stop 关闭机器人, 一旦关闭将无法使用，请联系程序员重新启动')



#interval to lock frequent reply
#sched to generate report

