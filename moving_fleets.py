#! /usr/bin/env python3
# coding: utf-8

import requests
import time
import re
import random
import math
import os
from bs4 import BeautifulSoup
from qqbot import qqbotsched


url_base = 'http://typhon.astroempires.com/'
url_set_language = '?lang=en'
url_login = 'login.aspx'
url_target = 'report.aspx?view=galaxy'
fleet_size_limit = 1000

headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language":"en-US,en;q=0.9"
}

params = {
	"email": "heye0507@gmail.com",
	"pass": "12345Abc",
	"navigator": "Netscape",
	"hostname": "typhon.astroempires.com",
	"javascript": "true",
	"post_back": "true"
}

target_params = {
	"galaxy": '23',
	"report_type": "moving_fleets"
}



def connect(url):
	write_to_file('----------连接服务器,请稍后---------')
	session = requests.Session()
	try:
		response = session.get(url,headers=headers,timeout=4)
	except requests.RequestException as e:
		print('connect:程序错误,清理未完成文件')
		print('debug: ',e)
		exit(0)
	#print (response.status_code)
	#print (response.cookies.get_dict())
	#print (response.text)
	time.sleep(2) #wait 2 seconds for next move
	return session

def login(session,url,data):
	try:
		response = session.post(url,data=data,headers=headers,timeout=4)
	except requests.RequestException as e:
		print('login:程序错误,清理未完成文件')
		print('debug: ',e)
		exit(0)
	#print (response.status_code)
	#print (response.cookies)
	#print (response.text)
	write_to_file('------登陆成功,2秒后自动搜索T20-29偷鸡----\n')
	time.sleep(2)
	return session

def getTarget(session,url,data):
	try:
		response = session.post(url,data=data,headers=headers,timeout=4)
	except requests.RequestException as e:
		print('getTarget:程序错误,清理未完成文件')
		print('debug: ',e)
		exit(0)
	#print (response.status_code)
	#print (response.cookies)
	soup = BeautifulSoup(response.content,'html.parser')
	tag = soup.find('table',class_='layout listing btnlisting tbllisting1 sorttable')
	report_enemy(tag)
	return session


#-----------------handle soup---------------
def has_td_but_no_keys(tag):
	return tag.has_attr('sorttable_customkey')

def no_fleets(tag):
	if (re.compile('No fleets').search(tag.get_text())):
		return True
	return False

def friendly_guild(tag):
	if(re.compile('(MOE|A.V|SR|NATO|RED)').search(tag.get_text())):
		return True
	return False

def not_report_data(enemy_list,fleet_size):
	if (int(enemy_list[2]) < 0):
		return True
	if (int(enemy_list[3]) <= fleet_size):
		return True
	return False

def write_to_file(enemy_info):
	with open('/Users/haohe/Desktop/moving_fleets_report.txt','a+') as f:
		for item in enemy_info:
			f.write(item+' ')#add a /n when counter counts to 0
		f.write('\n')

def report_enemy(soup):
	friendly_guild_counter = 0
	enemy_info = []
	for tag in soup.find_all('td'):
		if (no_fleets(tag)):
			write_to_file(tag.string)
		else:
			if (friendly_guild_counter is not 0):#skip friendly guild fields (5 attries)
				friendly_guild_counter = friendly_guild_counter - 1
				continue
			else: #check if it is friendly guild
				if (friendly_guild(tag)):
					friendly_guild_counter = 4
					continue
				else:
					if (len(enemy_info) is 5):
						if (not_report_data(enemy_info,fleet_size_limit)):
							enemy_info.clear()
						else:
							write_to_file(enemy_info)
							enemy_info.clear()
					if (not has_td_but_no_keys(tag)):
						enemy_info.append(re.sub(r'\s','',tag.a.string))
					else:
						enemy_info.append(tag['sorttable_customkey'])
	if (len(enemy_info) is 0):
		write_to_file('---------安全--------------')
	elif (not_report_data(enemy_info,fleet_size_limit)):
		write_to_file('---------安全--------------')
		enemy_info.clear()					
	else:
		write_to_file(enemy_info)
		enemy_info.clear()


#-----------------added--------------

@qqbotsched(hour='0-23',minute='0-57/3')
def mytask(bot):
	main()

def prepareData():
	with open('/Users/haohe/Desktop/moving_fleets_report.txt','r') as f:
		result = f.read()
	return result


def main():
	print('开始扫描,请等待')
	time_start = time.time()
	session = connect(url_base+url_set_language)
	session = login(session,url_base+url_login,params)
	galaxy_num = 20
	while (galaxy_num<30):
		target_params['galaxy'] = str(galaxy_num)
		print('-----正在寻找星系T'+target_params['galaxy']+'-------------')
		write_to_file('-----正在寻找星系T'+target_params['galaxy']+'-------------')
		session = getTarget(session,url_base+url_target,target_params)
		galaxy_num = galaxy_num + 1
		wait = random.randint(1,2)
		print('----等待'+str(wait)+'秒后查找下一星系--------\n')
		write_to_file('----等待'+str(wait)+'秒后查找下一星系--------\n')
		time.sleep(wait)
	session.close()
	write_to_file('------------关闭连接:完成--------')
	write_to_file('总耗时: '+str(math.floor(time.time()-time_start))+'秒\n')

if __name__ == '__main__':
	timeout = 5
	while True:
		try:
			if(timeout is 0):
				break
			if (os.path.isfile('/Users/haohe/Desktop/moving_fleets_report.txt')):
				print ('清理前序文件')
				os.remove('/Users/haohe/Desktop/moving_fleets_report.txt')
			main()
			#report = prepareData()
			#bot.SendTo(contact,report)
			break
		except KeyboardInterrupt:
			print('clearning files...')
			os.remove('/Users/haohe/Desktop/moving_fleets_report.txt')
			break
		except:
			os.remove('/Users/haohe/Desktop/moving_fleets_report.txt')
			timeout = timeout - 1
			if (timeout is not 0):
				print("不负责任猜测发生错误的原因是超时,10秒后重启下一轮链接")
				print("还剩%d次尝试" %timeout)
				time.sleep(5)
			else:
				print("尝试次数为0,程序终止")
				break
			pass





	