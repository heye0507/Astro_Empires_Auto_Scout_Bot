#! /usr/bin/env python3
# coding: utf-8

import requests
import time
import re
import random
import math
from bs4 import BeautifulSoup


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
	print ('----------连接服务器,请稍后---------')
	session = requests.Session()
	try:
		response = session.get(url,headers=headers,timeout=10)
	except requests.RequestException as e:
		print ('debug:程序错误,原因:'+e)
		exit(0)
	#print (response.status_code)
	#print (response.cookies.get_dict())
	#print (response.text)
	time.sleep(2) #wait 2 seconds for next move
	return session

def login(session,url,data):
	try:
		response = session.post(url,data=data,headers=headers,timeout=10)
	except requests.RequestException as e:
		print ('debug:程序错误,原因:'+e)
		exit(0)	
	#print (response.status_code)
	#print (response.cookies)
	#print (response.text)
	print ('------登陆成功,2秒后自动搜索T20-29偷鸡----\n')
	time.sleep(2)
	return session

def getTarget(session,url,data):
	try:
		response = session.post(url,data=data,headers=headers,timeout=10)
	except requests.RequestException as e:
		print ('debug:程序错误,原因:'+e)
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

def report_enemy(soup):
	friendly_guild_counter = 0
	enemy_info = []
	for tag in soup.find_all('td'):
		if (no_fleets(tag)):
			print(tag.string)
		else:
			if (friendly_guild_counter is not 0):
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
							print(enemy_info)
							enemy_info.clear()
					if (not has_td_but_no_keys(tag)):
						enemy_info.append(re.sub(r'\s','',tag.a.string))
					else:
						enemy_info.append(tag['sorttable_customkey'])
	if (len(enemy_info) is 0):
		print('---------安全--------------')
	elif (not_report_data(enemy_info,fleet_size_limit)):
		print('---------安全--------------')
		enemy_info.clear()					
	else:
		print(enemy_info)
		enemy_info.clear()


#-----------------added--------------



def main():
	time_start = time.time()
	session = connect(url_base+url_set_language)
	session = login(session,url_base+url_login,params)
	galaxy_num = 20
	while (galaxy_num<30):
		target_params['galaxy'] = str(galaxy_num)
		print('-----正在寻找星系T'+target_params['galaxy']+'-------------')
		session = getTarget(session,url_base+url_target,target_params)
		galaxy_num = galaxy_num + 1
		wait = random.randint(1,3)
		print ('----等待'+str(wait)+'秒后查找下一星系--------\n')
		time.sleep(wait)
	session.close()
	print('------------关闭连接:完成--------')
	print('总耗时: '+str(math.floor(time.time()-time_start))+'秒\n')

if __name__ == '__main__':
	main()