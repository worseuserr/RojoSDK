import os, subprocess, stat
from os.path import join
from datetime import datetime
from tools.Shell import Shell
from tools.Output import Output
from tools.Constants import BUILD, LIB,C_EMPHASIS,C_WARN,C_PRIMARY,C_GOOD,SETUP_FILE

class Build:
	def GetSource(libPath):
		Shell.ReadConfig()

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
				["git", "clone", "git@" + pair[0], "-b", pair[1], LIB + '/' + name],
				capture_output=True,
				text=True)
		else:
			result = subprocess.run(
				["git", "clone", "git@" + pair[0], LIB + '/' + name],
				capture_output=True,
				text=True)
		return (True)

	def Setup(config):
		Output.Write(f"{C_EMPHASIS}Performing first-time setup...\n")
		if (LIB == ""):
			raise ValueError("LIB is an empty string.")
		if (not os.path.exists("./" + BUILD)):
			os.mkdir("./" + BUILD)
			Output.Write(f"{C_PRIMARY}Created {BUILD} folder.\n")
		if (not os.path.exists("./" + LIB)):
			os.mkdir("./" + LIB)
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
		with open("./" + SETUP_FILE, 'w') as file:
			file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
				f"\nThis file marks {config["SDK_NAME"]} setup completion.")
		Output.Write(f"{C_GOOD}Setup complete.\n")

	def GetSources(config):
		pass

	def Build(sources):
		pass
