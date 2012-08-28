# -*- coding: utf-8 -*-
"""Poslatsms.cz gateway can be used to sending sms to T-Mobile CZ and Vodafone CZ"""

import urllib, urllib2
import re
import cookielib
from BaseGateway import *

from data.SMS import *

class Gateway(BaseGateway):
	def __init__(self, delegate):
		BaseGateway.__init__(self, delegate)
		#add headers needed by m.poslatsms.cz
		self.opener.addheaders.append( ('Referer', 'http://m.poslatsms.cz/'))
	
	@classmethod
	def getName(cls):
		return "PoslatSMS.cz"

	def getMaxLength(cls):
		return 160

	def _asyncSend(self, sms):
		#get timestamp needed by m.poslatsms.cz from my service
		ts = urllib.urlopen("http://freesmscz.appspot.com/timestamp").read()
		
		#send post request  
		postData = None
		if not sms.captchaCode:
			postData = urllib.urlencode({'timestamp' : ts, 'textsms' : sms.text, 'cislo-prijemce' : sms.toNum, 'cislo-odesilatele' : "", 'gateID' : '1', 'operatorID': "0"})
		else: #send with captcha
			postData = urllib.urlencode({'recaptcha_challenge_field': '', 'code':  sms.captchaCode, 'fromCaptcha': 'true', 'recipients' : '', 'notSplit' : '' , 'timestamp' : ts, 'textsms' : sms.text, 										'cislo-prijemce' : sms.toNum, 'cislo-odesilatele' : "", 'gateID' : '1', 'operatorID': "0"})
		respStr = self.opener.open('http://m.poslatsms.cz/?action=Send', postData).read()
		
		#check if message was successfully sent
		match = re.search("SMS odeslány!", respStr)
		if match:
				self.delegate.setSMSSent(sms)
				return

		#look for possible error messages
		match = re.findall('<h1>(.*?)</h1>', respStr, re.DOTALL)
		if match:
			error = match[0].strip()
			sms.error = error
			self.delegate.setSMSNotSent(sms)
			return
		
		#look for captcha
		match = re.findall("<div style=\"padding:5px;background:#efefef;\"><img src=\"(.*)\" />", respStr)
		if match:
			sms.captchaCode = None
			#get captcha url
			url = "http://m.poslatsms.cz%s" % match[0].strip()
			sms.captchaImageData = self.opener.open(url).read()
			self.delegate.showCaptcha(sms)
			while sms.captchaCode == None: #waiting until the user fills captcha
				pass
			if sms.captchaCode == "cancel": # sending was canceled
				sms.error = "SMS nebyla odeslána!"
				self.delegate.setSMSNotSent(sms)
				return
			else: # resend SMS with filled captcha
				self.sendSMS(sms)

		
