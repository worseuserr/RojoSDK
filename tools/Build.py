import shutil
import os, subprocess, stat
from os.path import join
from datetime import datetime
from tools.Shell import Shell
from tools.Output import Output
from tools.Constants import BUILD, C_BAD, DEBUG_DELETE_LIB, LIB,C_EMPHASIS,C_WARN,C_PRIMARY,C_GOOD,SETUP_FILE, SOURCE

class Build:
	def GetSource(libPath):
		pass

	def RemoveReadonly(func, path, exc):
		os.chmod(path, stat.S_IWRITE)
		if (Output.LogLevel == "verbose"):
			Output.Write(f"{C_WARN}\t{path} permissions overridden for deletion.\n")
		func(path)

	def GitClone(dep):
		pair = str.split(dep, '@')
		name = str.split(pair[0], '/')[1]
		branch = pair[1] if (len(pair) > 1) else False
		if (os.path.exists(join("./", LIB, name))):
			return (False)
		if (branch):
			result = subprocess.run(
				["git", "submodule", "add", "--force", "-b", pair[1], "git@" + pair[0], join('./', LIB, name)],
				capture_output=True,
				text=True)
		else:
			result = subprocess.run(
				["git", "submodule", "add", "--force", "git@" + pair[0], join('./', LIB, name)],
				capture_output=True,
				text=True)
		if (Output.LogLevel == "verbose" and len(result.stdout) > 0):
			Output.Write(f"\n{C_WARN}\tGit: {result.stdout.rstrip('\n')}")
		if (result.returncode != 0):
			Output.Write(f"\n{C_BAD}\tGit error: Code {result.returncode}\nGit: {result.stderr}")
			exit(code=1)
		return (True)

	def Setup(config):
		Output.Write(f"{C_EMPHASIS}Performing first-time setup...\n")
		if (LIB == ""):
			raise ValueError("LIB is an empty string.")
		if (not os.path.exists(join("./", BUILD))):
			os.mkdir(join("./", BUILD))
			Output.Write(f"{C_PRIMARY}Created {BUILD} folder.\n")
		if (os.path.exists(join("./", LIB)) and DEBUG_DELETE_LIB):
			shutil.rmtree("./" + LIB, onexc=Build.RemoveReadonly)
			Output.Write(f"{C_PRIMARY}Cleared existing {LIB} folder.\n")
		if (not os.path.exists(join("./", LIB))):
			os.mkdir(join("./", LIB))
		if (DEBUG_DELETE_LIB):
			with open(join("./", LIB, ".gitkeep"), 'w') as fp:
				pass
			Output.Write(f"{C_PRIMARY}Created new .gitkeep.\n")
		Output.Write(f"{C_PRIMARY}Created {LIB} folder.\n")
		if (len(config["Dependencies"]) > 0):
			Output.Write(f"{C_PRIMARY}Dependencies: [\n")
			for dep in config["Dependencies"]:
				Output.Write(f"{C_EMPHASIS}\t\'{dep}\'\n")
			Output.Write("]\n")
			Output.Write("Fetching repositories...\n")
			for dep in config["Dependencies"]:
				Output.Write(f"{C_EMPHASIS}\tCloning {dep}...")
				if (Build.GitClone(dep)):
					Output.WriteInPlace(f"{C_EMPHASIS}\tCloning {dep}... {C_GOOD}OK\n")
				else:
					Output.WriteInPlace(f"{C_EMPHASIS}\tCloning {dep}... {C_WARN}ALREADY PRESENT\n")
			Output.Write(f"{C_PRIMARY}Dependencies cloned.\n")
		else:
			Output.Write(f"{C_PRIMARY}Dependencies: []\n")
			Output.Write(f"{C_WARN}No git dependencies found, proceeding.\n")
		with open(join("./", SETUP_FILE), 'w') as file:
			file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
				f"\nThis file marks {config["SDK_NAME"]} setup completion.")
		Output.Write(f"{C_GOOD}Setup complete.\n")

	def GetSources(config):
		sources = set()
		for source in os.listdir(join("./", LIB)):
			path = join("./", LIB, source, SOURCE)
			if (os.path.isdir(path)):
				sources.add(path)
		return (sources)

	def Cleanup(config):
		pass

	def Build(sources):
		Output.Write(f"{C_EMPHASIS}Starting build...\n")
		seenDestPaths = set()
		build = join("./", BUILD)
		src = join("./", SOURCE)
		if (not os.path.exists(join("./", BUILD))):
			os.makedirs(build, exist_ok=True)
			Output.Write(f"{C_PRIMARY}Created build folder.\n")
		for sourceRoot in [src] + sources:
			Output.Write(f"{C_PRIMARY}\tProcessing: {sourceRoot}...")
			for dirpath, _, filenames in os.walk(sourceRoot):
				for filename in filenames:
					if (filename == ".gitkeep"):
						if (Output.LogLevel == "verbose"):
							Output.Write(f"{C_WARN}\tIgnoring .gitkeep in '{sourceRoot}'.\n")
						continue
					srcPath = os.path.join(dirpath, filename)
					relativePath = os.path.relpath(srcPath, start=sourceRoot)
					destPath = os.path.join(build, relativePath)
					if (destPath in seenDestPaths):
						Output.Write(f"{C_BAD}Build failed: File '{relativePath}' exists in multiple sources.\n")
						exit(code=1)
					seenDestPaths.add(destPath)
					os.makedirs(os.path.dirname(destPath), exist_ok=True)
					shutil.copy2(srcPath, destPath)
					if (Output.LogLevel == "verbose"):
						Output.Write(f"{C_PRIMARY}\t\tCopied: {srcPath}")
			Output.WriteInPlace(f"{C_PRIMARY}\tProcessing: {sourceRoot}... {C_GOOD}OK\n")
