# -*- coding: utf-8 -*-
"""startup.py a FreeSMS CLI processor
- it gets the commandline arguments and decides what to do
"""
import argparse

class Startup():
	def __init__(self):
		parser = argparse.ArgumentParser(description="FreeSMS Copyright (C) 2012 Kryštof Celba <kristofc97@gmail.com>")
		parser.add_argument('-p',
							help="specify platform", default="CLI",
							action="store", choices=["harmattan", "CLI"])
		parser.add_argument('-d',
							help="debug", default="0",
							action="store_true")


		self.args = parser.parse_args()

