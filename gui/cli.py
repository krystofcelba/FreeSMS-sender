# -*- coding: utf-8 -*-
import sys, os

import FreeSMS

from data.SMS import *


CAPTCHA_PATH = "/tmp/captcha.png"


class gui():
	"""
	Main command line interface class
	"""

	def __init__(self, freeSms):
		self.freeSms = freeSms
		
	def showCaptcha(self, sms):
		fw = file(CAPTCHA_PATH, "wb")
		fw.write(sms.captchaImageData)
		fw.close()
		os.system("display " + CAPTCHA_PATH + " &")
		sms.captchaCode = raw_input("Please type the text in the picture: ")
		
	def setSMSSent(self, sms):
		print("SMS sent")
		
	def showError(self, sms):
		print("Error while sending SMS. Error: %s" % sms.error)
		
	def startMainLoop(self):
		sms = SMS()
		sms.gateway = int(raw_input("Please type ID of the gateway: "))
		sms.toNum = raw_input("Please type the recipient number: ")
		sms.text = raw_input("Please write SMS text: ")
		self.freeSms.sendSMS(sms)








