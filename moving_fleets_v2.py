#! /usr/bin/env python3
# coding: utf-8

import requests
import time
import re
import random
import math
import os,json
from bs4 import BeautifulSoup



url_base = 'http://typhon.astroempires.com/'
url_set_language = '?lang=en'
url_login = 'login.aspx'
url_target = 'report.aspx?view=galaxy'
fleet_size_limit = 1000
searching_period = 300 #search ninja every 3 mins
AE_timeout = 10 #AE server is bad... (to wait more time for server responses)
log_path = '/root/aeBot/moving_fleets_report.txt'

config_data = {
	'galaxyLower': '20',
	'galaxyUpper': '30'
}



headers = {
	"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language":"en-US,en;q=0.9"
}

params = {
	"email": "2378314127@qq.com",
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


#-----------------handle upload data--------
def loadConfig():
	#get path info
	current_working_dir = os.getcwd()
	current_working_dir = current_working_dir + '/config.txt'
	global config_data
	#check if file exists, if not exists,use default
	if (not os.path.isfile(current_working_dir)):
		return 

	with open(current_working_dir,'r') as f:
		data = json.load(f)

	for key in data:
		if (data[key]==''):
			continue
		config_data[key] = data[key]

#-----------------handle soup---------------
def has_td_but_no_keys(tag):
	return tag.has_attr('sorttable_customkey')

def no_fleets(tag):
	if (re.compile('No fleets').search(tag.get_text())):
		return True
	return False

def friendly_guild(tag):
	if(re.compile('(MOE|A.V|SR|NATO|RED|Retroben|ASAE)').search(tag.get_text())):
		return True
	return False

def not_report_data(enemy_list,fleet_size):
	if (int(enemy_list[2]) < 0):
		return True
	if (int(enemy_list[3]) <= fleet_size):
		return True
	return False

def write_to_file(enemy_info):
	with open(log_path,'a+') as f:
		for item in enemy_info:
			f.write(item+' ')
		f.write('\n')

def write_log(log_data):
	with open(log_path,'a+') as f:
		for item in log_data:
			f.write(item)#add a /n when counter counts to 0


def report_enemy(soup):
	friendly_guild_counter = 0
	enemy_info = []
	for tag in soup.find_all('td'):
		if (no_fleets(tag)):
			continue
			#write_to_file(tag.string) #handle no fleets in your region, no need to report
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
						else: #found one enemy
							write_to_file(enemy_info)
							enemy_info.clear()
					if (not has_td_but_no_keys(tag)): #timer for arrival, not handled yet
						enemy_info.append(re.sub(r'\s','',tag.a.string))
					else:
						enemy_info.append(tag['sorttable_customkey'])
	if (len(enemy_info) is 0):
		print('---------安全--------------')
	elif (not_report_data(enemy_info,fleet_size_limit)):
		print('---------安全--------------')
		enemy_info.clear()					
	else:
		write_to_file(enemy_info)
		enemy_info.clear()


#-----------------added--------------



def run():
	print('开始扫描,请等待')
	print('----------连接服务器,请稍后---------')
	time_start = time.time()
	session = requests.Session()
	try:
		response = session.get(url_base+url_set_language,headers=headers,timeout=AE_timeout)
	except requests.RequestException as e:
		print('connect:程序错误,清理未完成文件')
		print('debug: ',e)
		exit(0)
	time.sleep(2)
	try:
		response = session.post(url_base+url_login,data=params,headers=headers,timeout=AE_timeout)
	except requests.RequestException as e:
		print('login:程序错误,清理未完成文件')
		print('debug: ',e)
		exit(0)
	time.sleep(2)
	loadConfig()
	print(config_data)
	galaxy_num = int(config_data['galaxyLower'])
	while (galaxy_num<int(config_data['galaxyUpper'])):
		target_params['galaxy'] = str(galaxy_num)
		print('-----正在寻找星系T'+target_params['galaxy']+'-------------')
		try:
			response = session.post(url_base+url_target,data=target_params,headers=headers,timeout=AE_timeout)
		except requests.RequestException as e:
			print('getTarget:程序错误,清理未完成文件')
			print('debug: ',e)
			exit(0)
		soup = BeautifulSoup(response.content,'html.parser')
		tag = soup.find('table',class_='layout listing btnlisting tbllisting1 sorttable')
		report_enemy(tag)
		galaxy_num = galaxy_num + 1
		wait = random.randint(1,2)
		if (galaxy_num is not int(config_data['galaxyUpper'])):
			print('----等待'+str(wait)+'秒后查找下一星系--------\n')
			#write_to_file('----等待'+str(wait)+'秒后查找下一星系--------\n')
			time.sleep(wait)
		elif (galaxy_num is int(config_data['galaxyUpper'])):
			print('扫描完成')
	session.close()
	print('------------关闭连接:完成--------')
	write_log('总耗时: '+str(math.floor(time.time()-time_start))+'秒\n')
	write_log('当前偷鸡被发现的最小规模为: '+str(fleet_size_limit)+'\n')



def main():
	timeout = 5
	while True:
		try:
			if(timeout is 0):
				print('critical issue: please contact author...')
				break
			if (os.path.isfile(log_path)):
				print ('清理上次记录文件')
				os.remove(log_path)
			run()
			next_search_time = time.asctime(time.localtime(time.time()+300))
			print ('下次搜索将在5分钟后进行,尝试次数设为5')
			write_log('下次搜索时间为: '+next_search_time+'\n')
			upper =int(config_data['galaxyUpper'])-1
			write_log('当前搜索范围为 %s - %s 星系\n' %(config_data['galaxyLower'],str(upper)))
			write_log('done\n')
			timeout = 5
			time.sleep(searching_period)
		except KeyboardInterrupt:
			print('clearning files...')
			#os.remove('/Users/haohe/Desktop/moving_fleets_report.txt')
			break
		except TypeError as e:
			print ('check type error')
			print (e)
			break
		except:
			timeout = timeout - 1
			if (timeout is not 0):
				print("不负责任猜测发生错误的原因是超时,10秒后重启下一轮链接")
				print("还剩%d次尝试" %timeout)
				time.sleep(5)
			else:
				write_log("已尝试连接AE服务器5次，全部失败...\n")
				print ('尝试次数5次, 将在下一轮重启连接')
				print ('下次搜索将在5分钟后进行,尝试次数设为5')
				next_search_time = time.asctime(time.localtime(time.time()+300))
				write_log('下次搜索时间为: '+next_search_time+'\n')
				write_log('done\n')
				timeout = 5
				time.sleep(searching_period)
			pass

if __name__ == '__main__':
	main()





