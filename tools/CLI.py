from enum import Enum
from tools.Output import Output
from tools.Constants import *

class Conflict(Enum):
	Error = 0
	Overlap = 1
	OK = 2 # For returning a non-conflicting arg

class ArgType(Enum):
	Bool = 0
	String = 1
	Int = 3
	StringArray = 4
	IntArray = 5

class CLI():
	UsageHint = f"Use {HELP_FLAG} for usage."

	class Group():
		Args = dict()

		def __init__(self, confictType, values):
			self.Values = dict()
			self.ConflictType = confictType
			for val in values:
				self.Values[val] = True
				if (not val in CLI.Group.Args):
					CLI.Group.Args[val] = list()
				CLI.Group.Args[val].append(self) # Store as hash lookup

		def __contains__(self, arg):
			return (arg in self.Values)

		@staticmethod
		def GetGroups(byArg):
			if (byArg in CLI.Group.Args):
				return (CLI.Group.Args[byArg])
			return (None)

		def Conflict(self, arg):
			if (arg not in self):
				return (Conflict.OK)
			elif (self.ConflictType == Conflict.Overlap):
				Output.Write(f"{C_WARN}{arg.Flag} shares overlapping functionality with {self.GetFlags(arg.Flag)}. {CLI.UsageHint}\n")
			elif (self.ConflictType == Conflict.Error):
				Output.Write(f"{C_BAD}Option {arg.Flag} cannot be used together with {self.GetFlags(arg.Flag)}. {CLI.UsageHint}\n")
			return (self.ConflictType)

		def GetFlags(self, excl):
			return ([k.Flag for k in self.Values if k.Flag != excl])

		def GetAlts(self, excl):
			return ([k.Alt for k in self.Values if k.Alt != excl])

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

		def GetDefaultValue(self):
			if (self.Type == ArgType.Bool):
				return (False)
			return (None)

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

	# Takes Arg object returned by AddArg
	def AddGroup(self, conflictType, *args):
		pass

	# Sets the resulting value of the arg to `key` in Parse()'s result, returns the Arg object
	def AddArg(self, flag, alt, key, argtype=ArgType.Bool):
		pass

	# Returns a dictionary with all keys set to the values entered in AddArg
	def Parse(self, argv):
		seenGroups = list()
		remaining = self.Args.copy()
		result = dict()
		i = 1 # Skip file arg
		while (i < len(argv)):
			arg = argv[i]
			i += 1
			obj = CLI.Arg.Get(arg)
			if (not obj):
				Output.Write(f"{C_BAD}Invalid option: \'{arg}\'. {CLI.UsageHint}\n")
				exit(code=1)
			for groups in seenGroups:
				for seen in groups:
					if (seen.Conflict(obj) == Conflict.Error):
						exit(code=1)
			group = CLI.Group.GetGroups(obj)
			if (group):
				seenGroups.append(group)
			remaining.remove(obj)
			result[obj.Key] = obj.GetValue(argv[i])
			if (obj.Type != ArgType.Bool):
				i += 1
		# Set the rest of the args to default values so you don't need to check if a key exists
		for obj in remaining:
			result[obj.Key] = obj.GetDefaultValue()
