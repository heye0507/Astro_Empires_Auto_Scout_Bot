# Astro_Empires_Auto_Scout_Bot
A auto scout and report bot (use Tencent QQ to report) for game Astro Empires

Designed for game Astro Empires. 

now is beta v0.3, supported Python3
UPDATES: 10/12/2018
1. Moved code and reconstruct on moving_fleets_v2.py for aliyun instance

set: 
log_path

email

pass

galaxy_num (if needed)

2.updated qqbot:
now supports:
-版本
which prints the current version of moving_fleets_v2.py 

mods: 
requests, beatifulSoup,qqbot

How to use:

1. open moving_fleets_v2.py
change url_base to your server, now set to typhon
change params email/pass to your account/password, eg: "email":"youraccount@gmail.com" "pass":"yourpassword"
scout galaxy now set to 20-29, you can change galaxy_num inside main() //poorly designed, will fix in later version
check the write_to_file and write_to_log function to set path correctly

once its done, on terminal, file folder, ./moving_fleets.py to start the program. 

the program will start scout galaxy T2x, once its done, it will creat a file named moving_fleets_report.txt in your path folder
it will sleep for 5mins for another scout (block)


2. connect to Tencent QQ for bot to auto report
you need to install qqbot (pip3 install qqbot)
refer to qqbot https://github.com/pandolia/qqbot for guide

copy the ae_report_bot.py file to qqbot plugin folder and run it as a qqbot plugin

it will automatically report to qq group "Astro Empire T服群", you can change this to your qq group
the timer is set to 6 mins for auto report.
support commands are 
-帮助 //this will list supportted command
-hello //test the bot is running
-报告 //reply for most recent scount report
--stop //kill the bot


做个记录, 目前完成的功能是
1. 每隔5分钟自动搜索T2x星系的偷鸡舰队
2. 可在qq群通过偷鸡机器人查看相关报告
3. 每6分钟检查一次是否有偷鸡舰队，如果有汇报，如果没有不汇报

0.4版本计划加入排眼功能，2x星系的ss
