from enum import Enum
from tools.Output import Output
from tools.Constants import *

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

		def ConflictsWith(self, lst):
			pass

	class Arg():
		Flags = dict()
		Alts = dict()

		def __init__(self, flag, alt, key, type):
			self.Flag = flag
			self.Alt = alt
			self.Key = key
			self.Type = type
			CLI.Arg.Flags[flag] = self
			CLI.Arg.Alts[alt] = self

		def GetValue(self, nextArg):
			pass

		@staticmethod
		def Get(flagOrAlt):
			if (flagOrAlt in CLI.Arg.Flags):
				return (CLI.Arg.Flags[flagOrAlt])
			elif (flagOrAlt in CLI.Arg.Alts):
				return (CLI.Arg.Alts[flagOrAlt])
			return (None)

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
		seen = list()
		result = dict()
		i = 1 # Skip file arg
		while (i < len(argv)):
			arg = argv[i]
			i += 1
			obj = CLI.Arg.Get(arg)
			if (not obj):
				Output.Write(f"{C_BAD}Invalid option: \'{arg}\', use {HELP_FLAG} for usage.\n")
				exit(code=1)
			seen.append(obj)
			for group in self.Groups:
				if (group.ConflictsWith(seen)):
					exit(code=1)
			result[arg.Key] = arg.GetValue(argv[i])
			if (arg.Type != ArgType.Bool):
				i += 1
