import os, sys
from os.path import join
from tools.Shell import Shell
from tools.Output import Output
from tools.Build import Build
from tools.Constants import C_BAD,CONFIG_FILE,SETUP_FILE,FORCE_ALT,FORCE_FLAG,SKIP_ALT,SKIP_FLAG,VERBOSE_ALT,VERBOSE_FLAG,C_EMPHASIS

# INIT

argv = Shell.SplitFlags(sys.argv)

config = Shell.ReadConfig(join("./", CONFIG_FILE))
isFirstLaunch = not os.path.exists(join("./", SETUP_FILE))

force = FORCE_FLAG in argv or FORCE_ALT in argv
skip = SKIP_FLAG in argv or SKIP_ALT in argv

if (force and skip):
	Output.Write(f"{C_BAD}Error: {SKIP_FLAG} ({SKIP_ALT}) and {FORCE_FLAG} ({FORCE_ALT}) cannot be passed simultaneously. Use --help for usage.")
	exit(code=1)

if (force or (isFirstLaunch and not skip)):
	shouldSetup = True
else:
	shouldSetup = False

if (VERBOSE_FLAG in argv or VERBOSE_ALT in argv):
	Output.LogLevel = "verbose"
else:
	Output.LogLevel = config["LogLevel"]

# BUILD

Output.Write(f"{C_EMPHASIS}Started build using SDK version " + config["SDK_VERSION"] + "\n")
if (shouldSetup):
	Build.Setup(config)
sources = Build.GetSources(config)
Build.Build(sources)

