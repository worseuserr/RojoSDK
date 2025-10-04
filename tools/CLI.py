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

		def __init__(self, conflictType, values):
			self.Values = dict()
			self.ConflictType = conflictType
			for val in values:
				self.Values[val] = True
				if (not val in self.Args):
					self.Args[val] = list()
				self.Args[val].append(self) # Store as hash lookup

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
				Output.Write(f"{C_WARN}{arg.Flag} overlaps with {self.GetFlags(excl=arg.Flag)}; their effects may be redundant. {CLI.UsageHint}\n")
			elif (self.ConflictType == Conflict.Error):
				Output.Write(f"{C_BAD}Option {arg.Flag} cannot be used together with {self.GetFlags(excl=arg.Flag)}. {CLI.UsageHint}\n")
			return (self.ConflictType)

		def GetFlags(self, excl):
			return ([k.Flag for k in self.Values if k.Flag != excl])

		def GetAlts(self, excl):
			return ([k.Alt for k in self.Values if k.Alt != excl])

	class Arg():
		Flags = dict()
		Alts = dict()
		Keys = dict()

		def __init__(self, flag, alt, key, type):
			if (flag in self.Flags):
				Output.Write(f"{C_BAD}{flag} flag has already been assigned to an argument. ({self.Flags[flag].Flag}, {self.Flags[flag].Alt})\n")
				exit(code=1)
			if (alt in self.Alts):
				Output.Write(f"{C_BAD}{alt} alt flag has already been assigned to an argument. ({self.Alts[alt].Flag}, {self.Alts[alt].Alt})\n")
				exit(code=1)
			if (key in self.Keys):
				Output.Write(f"{C_BAD}{key} key has already been assigned to an argument. ({self.Keys[key].Flag}, {self.Keys[key].Alt})\n")
				exit(code=1)
			self.Flag = flag
			self.Alt = alt
			self.Key = key
			self.Type = type
			self.Flags[flag] = self
			self.Alts[alt] = self
			self.Keys[key] = self

		def GetValue(self, nextArg=None):
			if (self.Type == ArgType.Bool):
				return (True)
			return (None)

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
		self.ExclusiveArgs = list()

	# Takes Arg object returned by AddArg
	def AddGroup(self, conflictType, *args):
		self.Groups.append(CLI.Group(conflictType, args))

	# Sets the resulting value of the arg to `key` in Parse()'s result, returns the Arg object
	def AddArg(self, flag, alt, key, argtype=ArgType.Bool):
		result = CLI.Arg(flag, alt, key, argtype)
		self.Args.append(result)
		return (result)

	# Adds an exclusive argument, throwing a warning if any other flags are present
	# exclusive arguments cause Parse to only return that value
	def AddExclusiveArg(self, flag, alt, key, argtype=ArgType.Bool):
		result = CLI.Arg(flag, alt, key, argtype)
		self.ExclusiveArgs.append(result)
		return (result)

	# Returns a dictionary with all keys set to the values entered in AddArg
	def Parse(self, argv):
		seenGroups = list()
		remaining = self.Args + self.ExclusiveArgs
		result = dict()
		i = 1 # Skip file arg
		while (i < len(argv)):
			arg = argv[i]
			i += 1
			obj = CLI.Arg.Get(arg)
			if (not obj):
				Output.Write(f"{C_BAD}Invalid option: \'{arg}\'. {CLI.UsageHint}\n")
				exit(code=1)
			if (obj in self.ExclusiveArgs):
				if (len(argv) > 2): # -> Means its not the only option
					Output.Write(f"{C_WARN}{obj.Flag} ignores all other flags. {CLI.UsageHint}\n")
				return ({obj.Key: obj.GetValue(argv[i] if len(argv) > i else None)})
			for groups in seenGroups:
				for seen in groups:
					if (seen.Conflict(obj) == Conflict.Error):
						exit(code=1)
			group = CLI.Group.GetGroups(obj)
			if (group):
				seenGroups.append(group)
			remaining.remove(obj)
			if (obj.Type != ArgType.Bool):
				if (i >= len(argv)):
					Output.Write(f"{C_BAD}{obj.Flag} requires a parameter. {CLI.UsageHint}\n")
					exit(code=1)
				result[obj.Key] = obj.GetValue(argv[i])
				i += 1
			result[obj.Key] = obj.GetValue()
		# Set the rest of the args to default values so you don't need to check if a key exists
		for obj in remaining:
			result[obj.Key] = obj.GetDefaultValue()
		return (result)
