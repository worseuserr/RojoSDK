from datetime import datetime
from tools.Constants import *
from tools.Output import Output
from os.path import join
import os, ast, stat, shutil, tomllib, subprocess, time, threading

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

	def SafeClearDir(dir):
		if (not os.path.exists(dir)):
			Output.Write(f"{C_WARN}Tried to clear non-existant folder ({dir})\n")
			return
		for filename in os.listdir(dir):
			if (filename == ".gitkeep"):
				continue
			path = join(dir, filename)
			if (os.path.isdir(path)):
				if (os.path.exists(join(path, ".git"))):
					shutil.rmtree(path, onexc=Shell.RemoveReadonly)
				else:
					Output.Write(f"{C_WARN}{path} is not a Git repository and was not removed.\n")
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

	# Returns 0 on success, 1 if present, 2 if present but not a git repository
	def NewSubmodule(dep):
		pair = str.split(dep, '@')
		name = str.split(pair[0], '/')[1]
		branch = pair[1] if (len(pair) > 1) else False
		if (os.path.exists(join(".", LIB, name))):
			if (os.path.exists(join(".", LIB, name, ".git"))):
				return (1)
			return (2)
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
		return (0)

	def ClearSubmodule(relpath):
		if (os.path.isdir(join(".", ".git", "modules", relpath))):
			shutil.rmtree(join(".", ".git", "modules", relpath), onexc=Shell.RemoveReadonly)
		relpath = relpath.replace('\\', '/')
		for result in [
			subprocess.run(["git", "submodule", "deinit", "-f", relpath], text=True, capture_output=True),
			subprocess.run(["git", "rm", "-f", relpath], text=True, capture_output=True),
			subprocess.run(["git", "config", "--remove-section", "submodule." + relpath], text=True, capture_output=True),
			subprocess.run(["git", "config", "-f", ".gitmodules", "--remove-section", "submodule." + relpath], text=True, capture_output=True),
			]:
			if (Output.LogLevel == "verbose" and len(result.stdout+result.stderr) > 1):
				Output.Write(f"{C_WARN}\tGit: {result.stdout+result.stderr}")
		if (os.path.isfile(join(".", relpath, ".git"))):
			os.remove(join(".", relpath, ".git"))

	def GetConstants(path):
		with open(path, "r") as f:
			tree = ast.parse(f.read(), filename=path)
		constants = {}
		for node in tree.body:
			if (isinstance(node, ast.Assign)):
				for target in node.targets:
					if (isinstance(target, ast.Name)):
						if (isinstance(node.value, ast.Constant)):
							constants[target.id] = node.value.value
		return (constants)

	def PrettyRun(func, prepend="", **kwargs):
		def animate():
			nonlocal done
			chars = "|/-\\"
			i = 0
			while (not done):
				Output.WriteInPlace(f"{prepend}{chars[i % len(chars)]}")
				i += 1
				time.sleep(0.1)
		if (Output.LogLevel == "verbose"):
			return (func(**kwargs))
		done = False
		t = threading.Thread(target=animate)
		t.start()
		result = func(**kwargs)
		done = True
		t.join()
		Output.WriteInPlace(f"{prepend}  ") # Clear bar
		return (result)

	def ChangeRoot(fullpath, newroot):
		parts = fullpath.split(os.sep)
		if (len(parts) > 1):
			parts[1] = newroot
		return (os.sep.join(parts))

	def Compare(file1, file2):
		with open(file1, 'r') as f1, open(file2, 'r') as f2:
			return (f1.read() == f2.read())
		return (True)

	def SetTime(file):
		with open(file, "w") as f:
			f.write(datetime.now().isoformat())

	def GetTime(file):
		with open(file, "r") as f:
			return (datetime.fromisoformat(f.read().strip()))
