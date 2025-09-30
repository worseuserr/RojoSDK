import os, sys
from os.path import join
from tools.Shell import Shell
from tools.Output import Colors, Output
from tools.Build import Build
from tools.Constants import *
from tools.Usage import Usage

# INIT

argv = Shell.SplitFlags(sys.argv)
config = Shell.ReadConfig(join(".", CONFIG_FILE))

if (HELP_FLAG in argv or HELP_ALT in argv):
	print(Usage)
	exit(code=0)

if (VERSION_FLAG in argv or VERSION_ALT in argv):
	print(f"{C_EMPHASIS}Using {SDK_NAME} version {Colors.Yellow}{SDK_VERSION}{C_EMPHASIS} by worseuserr.{Colors.Reset}")
	exit(code=0)

isFirstLaunch = not os.path.exists(join(".", SETUP_FILE))
force = FORCE_FLAG in argv or FORCE_ALT in argv
skip = SKIP_FLAG in argv or SKIP_ALT in argv
reset = RESET_FLAG in argv or RESET_ALT in argv
noclean = NOCLEAN_FLAG in argv or NOCLEAN_ALT in argv
fclean = FCLEAN_FLAG in argv or FCLEAN_ALT in argv
shouldSetup = (force or reset) or (isFirstLaunch and not skip)

# OPTION COMPATS

if ((force or reset) and skip):
	Output.Write(f"{C_BAD}Error: {SKIP_FLAG} ({SKIP_ALT}) and {FORCE_FLAG if force else RESET_FLAG} ({FORCE_ALT if force else RESET_ALT}) cannot be passed simultaneously. Use {HELP_FLAG} or {HELP_ALT} for usage.\n")
	exit(code=1)

if (fclean and noclean):
	Output.Write(f"{C_WARN}Warn: {FCLEAN_FLAG} ({FCLEAN_ALT}) takes priority over {NOCLEAN_FLAG} ({NOCLEAN_ALT}). Use {HELP_FLAG} or {HELP_ALT} for usage.\n")

if ((fclean or force) and reset):
	Output.Write(f"{C_WARN}Warn: {FORCE_FLAG} ({FORCE_ALT}) and {FCLEAN_FLAG} ({FCLEAN_ALT}) are unnecessary with {RESET_FLAG} ({RESET_ALT}). Use {HELP_FLAG} or {HELP_ALT} for usage.\n")

if (VERBOSE_FLAG in argv or VERBOSE_ALT in argv):
	Output.LogLevel = "verbose"
else:
	Output.LogLevel = config["LogLevel"]

if (reset):
	fclean = True

# BUILD

Output.Write(f"{C_EMPHASIS}Started build using SDK version {SDK_VERSION}\n")

if (fclean):
	noclean = False
	Output.Write(f"{C_PRIMARY}Performing full clean...\n")
	Shell.ClearDir(join(".", BUILD))
	Output.Write(f"{C_PRIMARY}/{BUILD} cleared.\n")
	Shell.ClearDir(join(".", LIB))
	Output.Write(f"{C_PRIMARY}/{LIB} cleared.\n")
	if (os.path.exists(join(".", SETUP_FILE))):
		os.remove(join(".", SETUP_FILE))
		Output.Write(f"{C_PRIMARY}Removed setup marker.\n")
if (not noclean):
	Build.Cleanup(config)
if (fclean and not reset):
	Output.Write(f"{C_EMPHASIS}Full clean completed.\n")
	exit(code=0)

if (shouldSetup):
	Build.Setup(config)
sources = Build.GetSources(config)
Build.Build(sources)
