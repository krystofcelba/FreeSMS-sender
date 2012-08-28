# -*- coding: utf-8 -*-
import urllib, urllib2
import math
import cookielib
import re
import smtplib
import time

OPER_AUTO = '0'
OPER_VOD = '1'
OPER_O2 = '2'
OPER_TM = '3'


BAD_NUM = 0
BAD_SENDER_NUM = 1
SMS_SENDED = 3
NUM_NOT_VOD = 4
NUM_NOT_O2 = 5
NUM_NOT_TM = 6
LIMIT_OVER = 7
USER_BLOCKED = 8
CONNECTION_ERROR = 9
UNDEF_ERROR = 10
WRONG_AUTH = 11

cj = cookielib.CookieJar()
#proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 

opener.addheaders.append(('User-agent', "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko)Chrome/6.0.472.62 Safari/534.3"))

str_split = lambda v, l: [v[i*l:(i+1)*l] for i in range(int(math.ceil(len(v)/float(l))))]



def send_sms_poslatsms(number, sender_number, text, operator = OPER_AUTO):
	opener.addheaders.append( ('Referer', 'http://m.poslatsms.cz/'))
	#resp_str = urllib.urlopen("http://m.poslatsms.cz/").read()
	ts = str(int(time.mktime(time.localtime()))) #re.findall('name="timestamp" value="(.*)"', resp_str)[0]
	
	post_data = urllib.urlencode({'timestamp' : ts, 'textsms' : text, 'cislo-prijemce' : number, 'cislo-odesilatele' : sender_number, 'gateID' : '1', 'operatorID': operator})
	resp = opener.open('http://m.poslatsms.cz/?action=Send', post_data)
	resp_str = resp.read()
	print resp_str
	
	#match = re.search("SMS odeslány!", resp_str)
	#if match:
	#	return SMS_SENDED
	
	match = re.findall('<h1>(.*?)</h1>', resp_str, re.DOTALL)
	if match:
		#print match[0].strip()
		#return UNDEF_ERROR
		return match[0].strip()

def send_sms_o2(number, text, login, passw, code = None, sseid = None):
	opener.addheaders.append( ('Referer', 'http://sms.1188.cz/'))
	if sseid:
		opener.addheaders.append(('Cookie', 'SESSID1188='+sseid))
	logged = False
	resp = opener.open("http://sms.1188.cz/")
	print resp.info()
	resp_str = resp.read()
	#print resp_str
	if resp_str.find('<div id="smsLogout"') != -1:
		logged = True
		print logged
	
	if logged == False:
		post_data = urllib.urlencode({'username' : login, 'password' : passw})
		resp = opener.open('http://sms.1188.cz/sms/login', post_data)
		resp_str = resp.read()
		if resp_str.find('<span class="message wrong">') != -1:
			return WRONG_AUTH
	
	y = re.findall("HTMLElement.prototype.y = '([\w]+)';", resp_str)[0]
	hidden = re.findall("<input type=\"hidden\" name=\"" + y + "[\\w]+\" id=\"([\\w]+)\" />", resp_str)[0]
	
	post_data = urllib.urlencode({'receiver_phone' : number, 'text' : text, hidden : '1'})
	resp = opener.open('http://sms.1188.cz/sms/send', post_data)
	resp_str = resp.read()
	
	for cookie in cj:
		print "PHPSESSID: ", cookie.value
	
	if resp_str.find('<div class="captchaTitle">') != -1:
		print "captcha"
		if code:
			post_data = urllib.urlencode({'receiver_phone' : number, 'text' : text, hidden : '1', 'captcha': code})
			resp = opener.open('http://sms.1188.cz/sms/send', post_data)
			resp_str = resp.read()
		else:
			y = re.findall("HTMLElement.prototype.y = '([\w]+)';", resp_str)[0]
			hidden = re.findall("<input type=\"hidden\" name=\"" + y + "[\\w]+\" id=\"([\\w]+)\" />", resp_str)[0]
		
			image = file("captcha.png", "w")
			image.write(opener.open("http://sms.1188.cz/captcha/show.png").read())
			image.close()
			

	match = re.search("SMS odeslány!", resp_str)
	if match:
		return SMS_SENDED

	match = re.findall('<span class="message wrong">([\s\S]*?)<\/span>', resp_str, re.DOTALL)
	if match:
		print match[0].strip()
		return UNDEF_ERROR


def get_error_string(error_num):
	if error_num== BAD_NUM:
		return "Chybné číslo příjemce"
	elif error_num == BAD_SENDER_NUM:
		return "Chybné číslo odesílatele"
	elif error_num == SMS_SENDED:
		return "SMS byla odeslána"
	elif error_num == NUM_NOT_VOD:
		return "Číslo není v síti Vodafone"
	elif error_num == NUM_NOT_O2:
		return "Číslo není v síti O2"
	elif error_num == NUM_NOT_TM:
		return "Číslo není v síti T-Mobile"
	elif error_num == NUM_NOT_TM:
		return "Číslo není v síti T-Mobile"
	elif error_num == LIMIT_OVER:
		return "Denní limit příjemce přesažen"
	elif error_num == USER_BLOCKED:
		return "Příjemce je zablokován"
	elif error_num == CONNECTION_ERROR:
		return "Nelze se připojit k bráně"
	elif error_num == UNDEF_ERROR:
		return "Došlo k neznámé chybě"

	
				
		
				
		
		

	
	
	

	
