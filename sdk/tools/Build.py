import re
import shutil
import os, subprocess, stat
from os.path import join
from datetime import datetime, timedelta
import time
from tools.Shell import Shell
from tools.Output import Output
from tools.Constants import *

class Build:
	def CheckMissingDependencies(config):
		if (len(config["Dependencies"]) > 0):
			Output.Write(f"{C_PRIMARY}Dependencies: [\n")
			for dep in config["Dependencies"]:
				Output.Write(f"{C_EMPHASIS}\t\'{dep}\'\n")
			Output.Write("]\n")
			Output.Write("Fetching repositories...\n")
			for dep in config["Dependencies"]:
				Output.Write(f"{C_EMPHASIS}\tChecking {dep}...")
				result = Shell.PrettyRun(Shell.NewSubmodule, f"{C_EMPHASIS}\tChecking {dep}... ", dep=dep)
				if (result == 0):
					Output.WriteInPlace(f"{C_EMPHASIS}\tChecking {dep}... {C_GOOD}OK\n")
				elif (result == 1):
					Output.WriteInPlace(f"{C_EMPHASIS}\tChecking {dep}... {C_GOOD}PRESENT\n")
				elif (result == 2):
					Output.WriteInPlace(f"{C_EMPHASIS}\tChecking {dep}... {C_BAD}PRESENT; NOT A GIT REPOSITORY\n")
			Output.Write(f"{C_PRIMARY}Dependencies cloned.\n")
		else:
			Output.Write(f"{C_PRIMARY}Dependencies: []\n")
			Output.Write(f"{C_WARN}No git dependencies found, proceeding.\n")

	def Setup(config):
		Output.Write(f"{C_EMPHASIS}Performing first-time setup...\n")
		lib = join(".", LIB)
		build = join(".", BUILD)
		if (LIB == ""):
			raise ValueError("LIB is an empty string.")
		if (not os.path.exists(build)):
			os.mkdir(build)
			Output.Write(f"{C_PRIMARY}Created {BUILD} folder.\n")
		if (os.path.exists(lib) and DEBUG_DELETE_LIB):
			shutil.rmtree(lib, onexc=Shell.RemoveReadonly)
			Output.Write(f"{C_PRIMARY}Cleared existing {LIB} folder.\n")
		if (not os.path.exists(lib)):
			os.mkdir(lib)
		if (DEBUG_DELETE_LIB):
			with open(join(lib, ".gitkeep"), 'w') as fp:
				pass
			Output.Write(f"{C_PRIMARY}Created new .gitkeep.\n")
		Output.Write(f"{C_PRIMARY}Created {LIB} folder.\n")
		Build.CheckMissingDependencies(config)
		with open(join(".", SETUP_FILE), 'w') as file:
			file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
				f"\nThis file marks {SDK_NAME} setup completion.")
		Output.Write(f"{C_GOOD}Setup complete.\n")

	def UpdateSource(path, config):
		subprocess.run(["git", "fetch"], cwd=path, text=True, capture_output=True)
		branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=path, text=True, capture_output=True)
		if (branch.returncode != 0):
			Output.Write(f"{C_BAD}Git returned an error while fetching {path}: {branch.stderr}\n")
			return
		count = subprocess.run(["git", "rev-list", "--count", f"{branch.stdout.strip()}..origin/{branch.stdout.strip()}"], cwd=path, text=True, capture_output=True)
		if (count.returncode != 0):
			Output.Write(f"{C_BAD}Git returned an error while counting {path}: {branch.stderr}\n")
			return
		count = int(count.stdout.strip())
		if (count < 1):
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_GOOD}{path} is up-to-date.\n")
			return
		if (config["AutoUpdateDependencies"]):
			Output.Write(f"{C_WARN}\tUpdate: {path} is {count} commits behind HEAD, updating...")
			result = Shell.PrettyRun(subprocess.run, f"{C_WARN}\tUpdate: {path} is {count} commits behind HEAD, updating... ", args=["git", "pull"], cwd=path, text=True, capture_output=True)
			if (result.returncode != 0):
				Output.Write(f"{C_BAD}Git returned an error while updating {path}: {branch.stderr}\n")
				return
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_WARN}Git: {result.stdout}\n")
			Output.WriteInPlace(f"{C_WARN}\tUpdate: {path} is {count} commits behind HEAD, updating... {C_GOOD}OK\n")
		else:
			Output.Write(f"{C_WARN}\tUpdate: {path} is {count} commits behind HEAD.\n")

	def ShouldCheckDependencies(config, update=False):
		if (config["DependencyCheckFrequency"] == "on_build"):
			return (True)
		elif (config["DependencyCheckFrequency"] == "never"):
			return (False)
		if (not config["DependencyCheckFrequency"] == "daily"):
			Output.Write(f"{C_BAD}Error: DependencyCheckFrequency is set to an invalid value.")
			return (False)
		updateFile = join(".", UPDATE_FILE)
		if (not os.path.isfile(updateFile) or datetime.now() - Shell.GetTime(updateFile) >= timedelta(days=1)):
			if (update):
				Shell.SetTime(updateFile)
			return (True)

	def GetSource(path, config):
		const = join(path, "tools", "Constants.py")
		if (os.path.exists(const)):
			const = Shell.GetConstants(const)
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_WARN}Constants: {const}\n")
			subconfig = Shell.ReadConfig(join(path, const["CONFIG_FILE"]))
			script = join(const["SDK_SCRIPT"])
			if (os.path.exists(join(path, script))):
				src = join(path, const["BUILD"])
		else:
			dependencySources = list()
			for dep in config["DependencySources"]:
				dependencySources.append(join(path, dep))
			srcs = [join(path, SOURCE)] + dependencySources
			for src in srcs:
				if (not os.path.isdir(src)):
					continue
				if (Output.LogLevel == "verbose"):
					Output.Write(f"{C_WARN}Selected source for {path}: {src}\n")
				return (src)
			Output.Write(f"{C_BAD}Could not find any valid source directory for {path}\n")
			return
		# Update
		if ((config["NotifyOutdatedDependencies"] or config["AutoUpdateDependencies"]) and Build.ShouldCheckDependencies(config, True)):
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_PRIMARY}Checking {path} for updates...\n")
			if (os.path.exists(join(path, ".git"))):
				Build.UpdateSource(path, config)
		# Build
		result = subprocess.run(["python3", script], cwd=path, text=True, capture_output=True)
		if (result.returncode != 0):
			Output.Write(f"{C_BAD}{path} {script} error: {result.stderr}\n")
			exit(code=1)
		# if (Output.LogLevel == "verbose"):
		# 	Output.Write(f"{C_WARN}{path} {script} output: {result.stderr+result.stdout}\n")
		return (src)

	def GetSources(config):
		Output.Write(f"{C_PRIMARY}Getting sources from lib\\...\n")
		if ((config["NotifyOutdatedDependencies"] or config["AutoUpdateDependencies"]) and Build.ShouldCheckDependencies(config, False)):
			Output.Write(f"{C_PRIMARY}Checking for dependency updates...\n")
		sources = list()
		for source in os.listdir(join(".", LIB)):
			path = join(".", LIB, source)
			if (not os.path.isdir(path)):
				continue
			src = Build.GetSource(path, config)
			if (src):
				sources.append(src)
		return (sources)

	def Cleanup(config):
		Output.Write(f"{C_EMPHASIS}Performing cleanup...\n")
		submodules = str.splitlines(subprocess.run(["git", "config", "--file", ".gitmodules", "--get-regexp", "path"], text=True, capture_output=True).stdout)
		if (len(submodules) < 1):
			Output.Write(f"{C_WARN}No submodules to clean.\n")
			return
		for submodule in submodules:
			relpath = os.path.normpath(str.split(submodule, ' ')[1])
			path = join(".", relpath)
			name = re.split(r"[\\\/]", relpath)[1]
			if (not os.path.exists(path) or (not any(name in item for item in config["Dependencies"]) and config["AutoClearDependencies"])):
				Output.Write(f"{C_PRIMARY}\tClearing {relpath} entry...")
				Shell.PrettyRun(Shell.ClearSubmodule, f"{C_PRIMARY}\tClearing {relpath} entry... ", relpath=relpath)
				Output.WriteInPlace(f"{C_PRIMARY}\tClearing {relpath} entry... {C_GOOD}OK\n")
				continue
			if (Output.LogLevel == "verbose"):
				Output.Write(f"{C_PRIMARY}\tSubmodule {path} still exists in lib, skipping.\n")
		Output.Write(f"{C_EMPHASIS}Cleanup finished.\n")

	def Build(sources):
		Output.Write(f"{C_EMPHASIS}Building...\n")
		startTime = time.time()
		seenDestPaths = set()
		build = join(".", BUILD)
		src = join(".", SOURCE)
		tmp = join(".", TMP)
		if (not os.path.exists(build)):
			os.makedirs(build, exist_ok=True)
			Output.Write(f"{C_PRIMARY}Created {build} folder.\n")
		if (not os.path.exists(tmp)):
			os.makedirs(tmp, exist_ok=True)
			Output.Write(f"{C_PRIMARY}Created {tmp} folder.\n")
		for sourceRoot in [src] + sources:
			Output.Write(f"{C_PRIMARY}\tProcessing: {sourceRoot}...")
			count = sum(1 for _ in os.walk(sourceRoot))
			i = 0
			for dirpath, _, filenames in os.walk(sourceRoot):
				if (Output.LogLevel != "verbose"):
					Output.LoadingBar(30, count, i, " " * 10)
				i += 1
				for filename in filenames:
					if (filename == ".gitkeep"):
						if (Output.LogLevel == "verbose"):
							Output.Write(f"{C_WARN}\tIgnoring .gitkeep in '{sourceRoot}'.\n")
						continue
					srcPath = os.path.join(dirpath, filename)
					relativePath = os.path.relpath(srcPath, start=sourceRoot)
					destPath = os.path.join(tmp, relativePath)
					if (destPath in seenDestPaths):
						Output.WriteInPlace(f"{C_PRIMARY}\tProcessing: {sourceRoot}... {C_BAD}FAIL\n")
						Output.Write(f"{C_BAD}Build failed: File '{relativePath}' exists in multiple sources.\n")
						shutil.rmtree(tmp, onexc=Shell.RemoveReadonly)
						exit(code=1)
					seenDestPaths.add(destPath)
					os.makedirs(os.path.dirname(destPath), exist_ok=True)
					shutil.copy2(srcPath, destPath)
					if (Output.LogLevel == "verbose"):
						Output.Write(f"{C_PRIMARY}\t\tCopied: {srcPath} to {destPath}\n")
			Output.WriteInPlace(f"{C_PRIMARY}\tProcessing: {sourceRoot}... {C_GOOD}OK{" " * 10}\n")
		Output.Write(f"{C_PRIMARY}Clearing build folder...")
		Shell.ClearDir(build)
		Output.WriteInPlace(f"{C_PRIMARY}Clearing build folder... {C_GOOD} OK\n")
		Output.Write(f"{C_PRIMARY}Copying new files...")
		Shell.CopyDir(tmp, build)
		Output.WriteInPlace(f"{C_PRIMARY}Copying new files... {C_GOOD} OK\n")
		shutil.rmtree(tmp, onexc=Shell.RemoveReadonly)
		Output.Write(f"{C_PRIMARY}Removed {TMP}.\n")
		Output.Write(f"{C_EMPHASIS}Build completed in {time.time() - startTime:.4f} seconds.\n")
