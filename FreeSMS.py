#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import signal
import startup

import gateways
from data.SMS import *

# enable running this program from absolute path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class FreeSMS:
	def __init__(self):
		# parse startup arguments
		start = startup.Startup()
		self.args = start.args

		self.debug = self.args.d == True

		# get the platform ID string
		platformId = "harmattan"  #default harmattan
		if self.args.p:
			platformId = self.args.p
		

		#load gui
		self.gui = None
		if platformId == "harmattan":
			from gui import qml
			self.gui = qml.gui(self)

		#start main loop
		self.gui.startMainLoop()
			
	def setSMSSent(self, sms):
		if self.debug:
			print("SMS sent")		
	
	def setSMSNotSent(self, sms):
		if self.debug:
			print("Error while sending SMS. Error: %s" % sms.error)

	def showCaptcha(self, captcha):
		if self.debug:
			print("show captcha")
		self.gui.showCaptcha(captcha)

	def cancelSendingSMS(self):
		self.gate.cancelSending()

	def sendSMS(self, sms):
		if self.debug:
			print("Sending SMS. Text: %s, toNum: %s, gateway: %s" % (sms.text, sms.toNum, sms.gateway))
		self.gate = None
		self.currSMS = sms
		if sms.gateway == "PoslatSMS.cz":
			self.gate = gateways.PoslatsmsGateway.Gateway(self)
		elif sms.gateway == "O2 CZ":
			self.gate = gateways.O2CZGateway.Gateway(self)

		self.gate.sendSMS(self.currSMS)
		
			


if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal.SIG_DFL) #meego command line exit hack
	freeSMS = FreeSMS()
	
	






