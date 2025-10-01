import shutil
import os, subprocess, stat
from os.path import join
from datetime import datetime
import time
from tools.Shell import Shell
from tools.Output import Output
from tools.Constants import BUILD, C_BAD, DEBUG_DELETE_LIB, LIB,C_EMPHASIS,C_WARN,C_PRIMARY,C_GOOD, SDK_NAME,SETUP_FILE, SOURCE, TMP

class Build:
	def GetSource(libPath):
		pass

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
		if (len(config["Dependencies"]) > 0):
			Output.Write(f"{C_PRIMARY}Dependencies: [\n")
			for dep in config["Dependencies"]:
				Output.Write(f"{C_EMPHASIS}\t\'{dep}\'\n")
			Output.Write("]\n")
			Output.Write("Fetching repositories...\n")
			for dep in config["Dependencies"]:
				Output.Write(f"{C_EMPHASIS}\tCloning {dep}...")
				if (Shell.NewSubmodule(dep)):
					Output.WriteInPlace(f"{C_EMPHASIS}\tCloning {dep}... {C_GOOD}OK\n")
				else:
					Output.WriteInPlace(f"{C_EMPHASIS}\tCloning {dep}... {C_WARN}ALREADY PRESENT\n")
			Output.Write(f"{C_PRIMARY}Dependencies cloned.\n")
		else:
			Output.Write(f"{C_PRIMARY}Dependencies: []\n")
			Output.Write(f"{C_WARN}No git dependencies found, proceeding.\n")
		with open(join(".", SETUP_FILE), 'w') as file:
			file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
				f"\nThis file marks {SDK_NAME} setup completion.")
		Output.Write(f"{C_GOOD}Setup complete.\n")

	def GetSources(config): # Barebones version, needs building and update checking support
		sources = list()
		for source in os.listdir(join(".", LIB)):
			path = join(".", LIB, source, SOURCE)
			if (os.path.isdir(path)):
				sources.append(path)
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
			if (os.path.exists(path)):
				if (Output.LogLevel == "verbose"):
					Output.Write(f"{C_PRIMARY}\tSubmodule {path} still exists in lib, skipping.\n")
				continue
			Output.Write(f"{C_PRIMARY}\tClearing {relpath} entry...")
			Shell.ClearSubmodule(relpath)
			Output.WriteInPlace(f"{C_PRIMARY}\tClearing {relpath} entry... {C_GOOD}OK\n")
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
			for dirpath, _, filenames in os.walk(sourceRoot):
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
			Output.WriteInPlace(f"{C_PRIMARY}\tProcessing: {sourceRoot}... {C_GOOD}OK\n")
		Output.Write(f"{C_PRIMARY}Clearing build folder...")
		Shell.ClearDir(build)
		Output.WriteInPlace(f"{C_PRIMARY}Clearing build folder... {C_GOOD} OK\n")
		Output.Write(f"{C_PRIMARY}Copying new files...")
		Shell.CopyDir(tmp, build)
		Output.WriteInPlace(f"{C_PRIMARY}Copying new files... {C_GOOD} OK\n")
		shutil.rmtree(tmp, onexc=Shell.RemoveReadonly)
		Output.Write(f"{C_PRIMARY}Removed {TMP}.\n")
		Output.Write(f"{C_EMPHASIS}Build completed in {time.time() - startTime:.4f} seconds.\n")
