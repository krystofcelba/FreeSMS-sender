 # -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from PySide.QtCore import QObject
from PySide.QtGui import *
from PySide.QtDeclarative import *

import sys

import FreeSMS

from data.SMS import *

class CaptchaImageProvider(QDeclarativeImageProvider):
	"""
	Captcha image provider
	"""
	def __init__(self, gui):
		QDeclarativeImageProvider.__init__(self, QDeclarativeImageProvider.ImageType.Image)
		self.gui = gui

	def requestImage(self, pathId, size, requestedSize):
		return QImage.fromData(self.gui.captchaData) #return current captcha image


class QMLHelper(QObject):
	"""
	QML Helper class
	"""
	def __init__(self, freeSms):
		QObject.__init__(self)
		self.freeSms = freeSms
		self.rootObject = None

	@QtCore.Slot(str, str)
	def sendSMS(self, text, toNum):
		sms = SMS()
		sms.text = text
		sms.toNum = toNum
		#sms.gateway = "PoslatSMS.cz"
		sms.gateway = "O2 CZ"
		self.freeSms.sendSMS(sms)

	@QtCore.Slot()
	def cancelSendingSMS(self):
		self.freeSms.currSMS.captchaCode = "cancel" #cancel waiting for captcha code in SMS sending thread
		self.freeSms.cancelSendingSMS()

	@QtCore.Slot(str)
	def setCaptcha(self, code):
		self.freeSms.currSMS.captchaCode = code

	@QtCore.Slot()
	def showCaptcha(self):
		self.rootObject.showCaptcha() #show captcha dialog to user



class gui(QObject):
	"""
	Main QML gui class
	"""
	showCaptchaSignal = QtCore.Signal()

	def __init__(self, freeSms):
		QObject.__init__(self)
		self.freeSms = freeSms
		
	def showCaptcha(self, captcha):
		self.captchaData = captcha
		self.showCaptchaSignal.emit() #control gui must be in main thread
		
	def startMainLoop(self):
		self.app = QApplication(sys.argv) # create the application
		view = QDeclarativeView() # create the declarative view
		# add Python properties to the QML root context
		rc = view.rootContext()
		self.helper = QMLHelper(self.freeSms)
		rc.setContextProperty("helper", self.helper)
		rc.setContextProperty("debug", self.freeSms.debug)
		self.showCaptchaSignal.connect(self.helper.showCaptcha)


		# load main qml file
		view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
		view.setSource("gui/qml/Main.qml")

		self.rootObject = view.rootObject()
		self.helper.rootObject = self.rootObject
		
		#install python image provider 
		captchaProvider = CaptchaImageProvider(self)
		view.engine().addImageProvider("captcha", captchaProvider)
	
		view.window().showFullScreen()
		view.resize(480,854)
		view.show()
		self.app.exec_()
		








