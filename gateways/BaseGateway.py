# -*- coding: utf-8 -*-
"""Base SMS gateway"""

import urllib, urllib2
import cookielib
import threading

from data.SMS import *

def getCookieByName(cj, name):
    return [cookie for cookie in cj if cookie.name == name][0].value

class BaseGateway:
	def __init__(self, delegate):
		self.delegate = delegate
		#init urllib2 opener with cookie support
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj)) 
		self.opener.addheaders.append(('User-agent', "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko)Chrome/6.0.472.62 Safari/534.3"))
		self.downloadThread = None
	
	@classmethod
	def getName(cls):
		"""Gateway name"""
		return "BaseGateway"	
	
	@classmethod	
	def getMaxLength(cls):
		"""Max SMS length"""
		return 0
	

	def _asyncSend(self, sms):
		"""Asynchronous SMS send"""
		pass

	def cancelSending(self):
		"""Stop SMS sending thread"""
		self.downloadThread.join()

	def sendSMS(self, sms):
		self.downloadThread = threading.Thread(target=self._asyncSend, args=(sms, ))
		self.downloadThread.start()
		
