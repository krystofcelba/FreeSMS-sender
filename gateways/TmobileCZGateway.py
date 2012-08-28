# -*- coding: utf-8 -*-
"""T-Mobile CZ free gateway can be used to sending sms to T-Mobile CZ"""

import urllib, urllib2
import re
import cookielib
import time
from BaseGateway import *

from data.SMS import *

class Gateway(BaseGateway):
	def __init__(self, delegate):
		BaseGateway.__init__(self, delegate)
		self.opener.addheaders.append( ('Referer', 'http://sms.t-zones.cz/open.jsp'))

	def getName(self):
		return "T-Mobile CZ"

	def getMaxLength(self):
		return 160

	def _asyncSend(self, sms):
		if sms.captchaCode == None:
			self.opener.open('https://login.client.tmo.cz/um/cs/logout.jsp') #logout
			#get counter
			respStr = self.opener.open('http://sms.t-zones.cz/open.jsp').read()
			match = re.findall('<input type="hidden" name="counter" value="(.*?)" \/>', respStr, re.DOTALL)
			self.counter = match[0]
			self.startTime = time.time()
			#download captcha
			image = self.opener.open('http://sms.t-zones.cz/open/captcha.jpg').read()
			self.delegate.showCaptcha(image)
			while sms.captchaCode == None: #waiting until the user fills captcha
				pass
			if sms.captchaCode == "cancel": # sending was canceled
				sms.error = "SMS nebyla odeslána!"
				self.delegate.setSMSNotSent(sms)
				return
			else: # resend SMS with filled captcha
				self.sendSMS(sms)
		else:
			#wait 16s
			now = time.time()
			if self.startTime + 16 > now:
				time.sleep(self.startTime + 16 - now)
			
			postData = urllib.urlencode({'counter' : self.counter, 'recipient' : sms.toNum, 'text' : sms.text, 'send' : 'Odeslat', 'mtype' : '0', 'captcha' : sms.captchaCode})
			respStr = self.opener.open('http://sms.t-zones.cz/open.jsp?site=1', postData).read()
			#check if message was successfully sent
			match = re.search("(SMS zpr.va byl. odeslán.|SMS was sent)", respStr)
			if match:
				self.delegate.setSMSSent(sms)
				return

			#look for bad captcha
			match = re.search("Captcha does not match.", respStr)
			if match:
				sms.captchaCode = None
				self.sendSMS(sms)
				return
			
			#look for possible error messages
			match = re.findall('<p class="text-red.*?">(.*?)<\/p>', respStr, re.DOTALL)
			if match:
				error = match[0]
				sms.error = error
				self.delegate.setSMSNotSent(sms)
				return
			
			
		

		
