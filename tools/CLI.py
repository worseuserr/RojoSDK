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
	class Group():
		def __init__(self, confictType, values):
			self.Values = values
			self.ConflictType = confictType

	class Arg():
		def __init__(self, flag, alt, key, type):
			self.Flag = flag
			self.Alt = alt
			self.Key = key
			self.Type = type

	def __init__(self):
		self.Groups = list()
		self.Args = list()

	def AddGroup(self, conflictType, *args):
		pass

	# Sets the resulting value of the arg to `key` in Parse()'s result, returns the Arg object
	def AddArg(self, flag, alt, key, argtype=ArgType.Bool):
		pass

	# Returns a dictionary with all keys set to the values entered in AddArg
	def Parse(self, argv):
		pass
