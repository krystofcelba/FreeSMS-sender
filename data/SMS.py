
class SMS:
	"""Object representation of SMS message"""
	toNum = ""			# recipient number
	text = ""  			# SMS text
	gateway = 0		# gateway id
	captchaCode = None 	# captcha code
	captchaImageData = None # captcha image data
	error = "" 			# error while sending

	
