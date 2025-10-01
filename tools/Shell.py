import stat
import subprocess
from tools.Constants import *
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
		if (not os.path.exists(dir)):
			Output.Write(f"{C_WARN}Tried to clear non-existant folder ({dir})\n")
			return
		for filename in os.listdir(dir):
			if (filename == ".gitkeep"):
				continue
			path = join(dir, filename)
			if (os.path.isdir(path)):
				shutil.rmtree(path, onexc=Shell.RemoveReadonly)
			else:
				os.remove(path)
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_WARN}\tRemoved {path}\n")

	def CopyDir(dir, target):
		if (not os.path.exists(target)):
			Output.Write(f"{C_WARN}Tried to copy to non-existant folder ({dir} -> {target})\n")
			return
		for filename in os.listdir(dir):
			src = join(dir, filename)
			dst = join(target, filename)
			if os.path.isdir(src):
				shutil.copytree(src, dst, dirs_exist_ok=True)
			else:
				shutil.copy2(src, dst)
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_WARN}\tCopied {src} to {dst}\n")

	def RemoveReadonly(func, path, exc):
		os.chmod(path, stat.S_IWRITE)
		if (Output.LogLevel == "verbose"):
			Output.Write(f"{C_WARN}\t{path} permissions overridden for deletion.\n")
		func(path)

	def NewSubmodule(dep):
		pair = str.split(dep, '@')
		name = str.split(pair[0], '/')[1]
		branch = pair[1] if (len(pair) > 1) else False
		if (os.path.exists(join(".", LIB, name))):
			return (False)
		if (branch):
			result = subprocess.run(
				["git", "submodule", "add", "--force", "-b", pair[1], "git@" + pair[0], join('.', LIB, name)],
				capture_output=True,
				text=True)
		else:
			result = subprocess.run(
				["git", "submodule", "add", "--force", "git@" + pair[0], join('.', LIB, name)],
				capture_output=True,
				text=True)
		if (Output.LogLevel == "verbose" and len(result.stdout) > 0):
			Output.Write(f"\n{C_WARN}\tGit: {result.stdout.rstrip('\n')}")
		if (result.returncode != 0):
			Output.Write(f"\n{C_BAD}Git error: Code {result.returncode}\nGit: {result.stderr}")
			exit(code=1)
		subprocess.run(["git", "restore", "--staged", ".gitmodules"], capture_output=True, text=True)
		subprocess.run(["git", "restore", "--staged", join(LIB, name)], capture_output=True, text=True)
		return (True)

	def ClearSubmodule(relpath):
		if (os.path.isdir(join(".", ".git", "modules", relpath))):
			shutil.rmtree(join(".", ".git", "modules", relpath), onexc=Shell.RemoveReadonly)
		relpath = relpath.replace('\\', '/')
		result = subprocess.run(["git", "submodule", "deinit", "-f", relpath], text=True, capture_output=True)
		if (Output.LogLevel == "verbose" and len(result.stdout+result.stderr) > 1):
			Output.Write(f"{C_WARN}\tGit: {result.stdout+result.stderr}")
		result = subprocess.run(["git", "rm", "-f", relpath], text=True, capture_output=True)
		if (Output.LogLevel == "verbose" and len(result.stdout+result.stderr) > 1):
			Output.Write(f"{C_WARN}\tGit: {result.stdout+result.stderr}")
		result = subprocess.run(["git", "config", "--remove-section", "submodule." + relpath], text=True, capture_output=True)
		if (Output.LogLevel == "verbose" and len(result.stdout+result.stderr) > 1):
			Output.Write(f"{C_WARN}\tGit: {result.stdout+result.stderr}")
		result = subprocess.run(["git", "config", "-f", ".gitmodules", "--remove-section", "submodule." + relpath], text=True, capture_output=True)
		if (Output.LogLevel == "verbose" and len(result.stdout+result.stderr) > 1):
			Output.Write(f"{C_WARN}\tGit: {result.stdout+result.stderr}")
