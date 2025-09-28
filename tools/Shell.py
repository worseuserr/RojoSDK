import os, json, io, tomllib

class Shell:
	def ReadConfig(path):
		with open(path, "rb") as file:
			return (tomllib.load(file)["build"])

	def SplitFlags(flags):
		result = []
		for flag in flags:
			if flag.startswith("--"):
				result.append(flag)
			elif flag.startswith("-") and len(flag) > 2:
				result.extend([f"-{c}" for c in flag[1:]])
			else:
				result.append(flag)
		return (result)

