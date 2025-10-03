from enum import Enum

class Conflict(Enum):
	Error = 0
	Warn = 1

class ArgType(Enum):
	Bool = 0
	String = 1
	Int = 3
	StringArray = 4
	IntArray = 5

class CLI():
	def __init__(self):
		self.Groups = list()

	def AddGroup(self, conflictType, *values):
		pass

	# Sets the resulting value of the arg to `key` in Parse()'s result
	def AddArg(self, flag, alt, key, argtype=ArgType.Bool):
		pass

	# Returns a dictionary with all keys set to the values entered in AddArg
	def Parse(self, argv):
		pass
