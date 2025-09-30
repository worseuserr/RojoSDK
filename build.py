import os, sys
from os.path import join
from tools.Shell import Shell
from tools.Output import Colors, Output
from tools.Build import Build
from tools.Constants import C_BAD, C_WARN, CLEAN_ALT, CLEAN_FLAG,CONFIG_FILE, HELP_ALT, HELP_FLAG, RESET_ALT, RESET_FLAG, SDK_NAME, SDK_VERSION,SETUP_FILE,FORCE_ALT,FORCE_FLAG,SKIP_ALT,SKIP_FLAG,VERBOSE_ALT,VERBOSE_FLAG,C_EMPHASIS, VERSION_ALT, VERSION_FLAG
from tools.Usage import Usage

# INIT

argv = Shell.SplitFlags(sys.argv)
config = Shell.ReadConfig(join("./", CONFIG_FILE))

if (HELP_FLAG in argv or HELP_ALT in argv):
	print(Usage)
	exit(code=0)

if (VERSION_FLAG in argv or VERSION_ALT in argv):
	print(f"{C_EMPHASIS}Using {SDK_NAME} version {Colors.Yellow}{SDK_VERSION}{C_EMPHASIS} by worseuserr.{Colors.Reset}")
	exit(code=0)

isFirstLaunch = not os.path.exists(join("./", SETUP_FILE))
force = FORCE_FLAG in argv or FORCE_ALT in argv
skip = SKIP_FLAG in argv or SKIP_ALT in argv
reset = RESET_FLAG in argv or RESET_ALT in argv
clean = CLEAN_FLAG in argv or CLEAN_ALT in argv
shouldSetup = (force or reset) or (isFirstLaunch and not skip)

# OPTION COMPATS

if ((force or reset) and skip):
	Output.Write(f"{C_BAD}Error: {SKIP_FLAG} ({SKIP_ALT}) and {FORCE_FLAG if force else RESET_FLAG} ({FORCE_ALT if force else RESET_ALT}) cannot be passed simultaneously. Use {HELP_FLAG} or {HELP_ALT} for usage.\n")
	exit(code=1)

if (clean and (force or reset or skip)):
	Output.Write(f"{C_WARN}Warn: {CLEAN_FLAG} ({CLEAN_ALT}) ignores other flags. Use {HELP_FLAG} or {HELP_ALT} for usage.\n")

if (force and reset):
	Output.Write(f"{C_WARN}Warn: {FORCE_FLAG} ({FORCE_ALT}) is unnecessary with {RESET_FLAG} ({RESET_ALT}) Use {HELP_FLAG} or {HELP_ALT} for usage.\n")

if (VERBOSE_FLAG in argv or VERBOSE_ALT in argv):
	Output.LogLevel = "verbose"
else:
	Output.LogLevel = config["LogLevel"]

# BUILD

if (reset or clean):
	Build.Cleanup(config)
if (clean):
	exit(code=0)

Output.Write(f"{C_EMPHASIS}Started build using SDK version {SDK_VERSION}\n")
if (shouldSetup):
	Build.Setup(config)
sources = Build.GetSources(config)
Build.Build(sources)
