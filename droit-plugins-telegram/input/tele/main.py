# main.py - telegram-plugins-telegram.input.tele
# A plugin for python-droit (telepyd)
#
# Copyright 2020 - Jakob Stolze
#
# This file is part of telepyd (https://github.com/jarinox/telepyd)
#
# Example:
# TELE*cmd!start			true if the /start command is entered by the user
# TELE*default! 			always true but with a low ranking (use for default response)


def block(userinput, iN, name, db):
	passRule = False
	rankMod = 0
	outVars = {}

	inputRules = db.rules[iN].input


	for rule in inputRules:
		if(rule.tag == name):
			if(db.temp["cmd"]):
				if(rule.attrib["option"] == "cmd"): # cmd
					if(" ".join(rule.children) in userinput.words):
						passRule = True
						rankMod = 10
			
			elif(db.temp["callback"]):
				if(rule.attrib["option"] == "callback"): # callback
					if(rule.children[0] + rule.children[1] == db.temp["callback"]):
						passRule = True
						rankMod = 10

			elif(rule.attrib["option"] == "default"): # default
				passRule = True
				rankMod = -20

	return passRule, outVars, rankMod, db