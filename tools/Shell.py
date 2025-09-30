import stat
from tools.Constants import C_WARN
from tools.Output import Output
from os.path import join
import os
import shutil
import tomllib

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

	def ClearDir(dir):
		for filename in os.listdir(dir):
				if (filename == ".gitkeep"):
					continue
				path = join(dir, filename)
				if (os.path.isfile(path) or os.path.islink(path)):
					os.remove(path)
				elif (os.path.isdir(path)):
					shutil.rmtree(path, onexc=dir.RemoveReadonly)
				else:
					continue
				if (Output.LogLevel != "verbose"):
					Output.Write(f"{C_WARN}\tRemoved {path}\n")

	def CopyDir(dir, target):
		if (not os.path.exists(target)):
			Output.Write(f"{C_WARN}Tried to copy to non-existant folder ({dir} -> {target})\n")
			return
		for item in os.listdir(dir):
			src = join(dir, item)
			dst = join(target, item)
			if os.path.isdir(src):
				shutil.copytree(src, dst, dirs_exist_ok=True)
			else:
				shutil.copy2(src, dst)

	def RemoveReadonly(func, path, exc):
		os.chmod(path, stat.S_IWRITE)
		if (Output.LogLevel == "verbose"):
			Output.Write(f"{C_WARN}\t{path} permissions overridden for deletion.\n")
		func(path)
