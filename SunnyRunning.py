# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import requests
import json
import time
import hashlib
import random
import sys
import smtplib

from email.mime.text import MIMEText
from email.header import Header

# Input Your IMEI Code Here
IMEI = ''

def MD5(s):
    return hashlib.md5(s.encode()).hexdigest()


def encrypt(s):
    result = ''
    for i in s:
        result += table[ord(i) - ord('0')]
    # print(result)
    return result

# 发送邮件
def mail():
	# 第三方 SMTP 服务.具体设置参数请参考邮箱服务商的设置
	mail_host="smtp.xxx.com"  # 设置服务器
	mail_user=""    # 用户名
	mail_pass="."   # 口令

	sender = 'xxx@xxx.com'
	receivers = ['xxx@xxx.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

	message = MIMEText('汉姆出现问题', 'plain', 'utf-8')
	message['From'] = "xxx<xxx@xxx.com>"
	message['To'] =  "xxx<xxx@xxx.com>"

	subject = '汉姆出现问题'
	message['Subject'] = Header(subject, 'utf-8')

	smtpObj = smtplib.SMTP_SSL()
	smtpObj.connect(mail_host, 465)    # 465 为 SMTP 的 ssl 端口号
	smtpObj.login(mail_user,mail_pass)
	smtpObj.sendmail(sender, receivers, message.as_string())
	print("邮件发送成功")


if (len(IMEI) != 32):
    exit("IMEI Format Error!")

# Generate table Randomly
alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(alphabet)
table = ''.join(alphabet)[:10]

API_ROOT = 'http://client3.aipao.me/api'
Version = '2.14'

# Generate Runnig Data Randomly
RunTime = str(random.randint(720, 1000))  # seconds
# RunDist = str(2000 + random.randint(0, 3))  # meters
RunDist = str(1600 + random.randint(0, 3))  # meters
RunStep = str(random.randint(1300, 1600))  # steps

# Login
TokenRes = requests.get(
    API_ROOT + '/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI)
TokenJson = json.loads(TokenRes.content.decode('utf8', 'ignore'))
print(TokenJson)

# Headers
# If Token Error, Then Send E-Mail
try:
	token = TokenJson['Data']['Token']
except:
	mail()
	exit(1)

userId = str(TokenJson['Data']['UserId'])
timespan = str(time.time()).replace('.', '')[:13]
auth = 'B' + MD5(MD5(IMEI)) + ':;' + token
nonce = str(random.randint(100000, 10000000))
sign = MD5(token + nonce + timespan + userId).upper()  # sign为大写

header = {'nonce': nonce, 'timespan': timespan,
          'sign': sign, 'version': Version, 'Accept': None, 'User-Agent': None, 'Accept-Encoding': None,
          'Connection': 'Keep-Alive'}

# Start Running
SRSurl = API_ROOT + '/' + token + '/QM_Runs/SRS?S1=30.534738&S2=114.367788&S3=2000'
SRSres = requests.get(SRSurl, headers=header, data={})
SRSjson = json.loads(SRSres.content.decode('utf8', 'ignore'))

# Running Sleep
StartT = time.time()
for i in range(int(RunTime)):
    time.sleep(1)
    print("Current Minutes: %d Running Progress: %.2f%%\r" %
        (i / 60, i * 100.0 / int(RunTime)), end='')
print("")
print("Running Seconds:", time.time() - StartT)

# print(SRSurl)
# print(SRSjson)

RunId = SRSjson['Data']['RunId']

# End Running
EndUrl = API_ROOT + '/' + token + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
         encrypt(RunTime) + '&S5=' + encrypt(RunDist) + \
         '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(RunStep)

EndRes = requests.get(EndUrl, headers=header)
EndJson = json.loads(EndRes.content.decode('utf8', 'ignore'))

print("-----------------------")
print("Time:", RunTime)
print("Distance:", RunDist)
print("Steps:", RunStep)
print("-----------------------")

if (EndJson['Success']):
    print("[+]OK:", EndJson['Data'])
else:
    print("[!]Fail:", EndJson['Data'])
