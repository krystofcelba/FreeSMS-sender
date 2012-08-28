# -*- coding: utf-8 -*-
"""smszdarma.org free gateway can be used to sending sms to O2 CZ"""

import urllib, urllib2
import re
import cookielib
from BaseGateway import *

from data.SMS import *

class Gateway(BaseGateway):
	def __init__(self, delegate):
		BaseGateway.__init__(self, delegate)
		self.opener.addheaders.append( ('Referer', 'http://smszdarma.org/'))

	@classmethod
	def getName(cls):
		return "smszdarma.org"

	@classmethod
	def getMaxLength(cls):
		return 500

	def _asyncSend(self, sms):
		postData = urllib.urlencode({'operator' : 'o2', 'to' : sms.toNum, 'message' : sms.text, 'ref' : 'smszdarma.org'})
		respStr = self.opener.open('http://www.smszdarma.org/sms/sms.php', postData).read()
		#check if message was successfully sent
		match = re.search("Odeslána SMS na O2.", respStr)
		if match:
			self.delegate.setSMSSent(sms)
			return
		else:
			sms.error = "SMS nebyla odeslána!"
			self.delegate.setSMSNotSent(sms)
			
			
		

		
