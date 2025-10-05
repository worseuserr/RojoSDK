import os, sys
from os.path import join
from tools.CLI import *
from tools.Shell import Shell
from tools.Output import Colors, Output
from tools.Build import Build
from tools.Constants import *
from tools.Usage import Usage

# INIT

config = Shell.ReadConfig(join(".", CONFIG_FILE))
argv = Shell.SplitFlags(sys.argv + config["BuildOptions"])
cli = CLI()

a_Skip=			cli.AddArg(SKIP_FLAG, SKIP_ALT, "Skip")
a_Force=		cli.AddArg(FORCE_FLAG, FORCE_ALT, "Force")
a_Verbose=		cli.AddArg(VERBOSE_FLAG, VERBOSE_ALT, "Verbose")
a_Reset=		cli.AddArg(RESET_FLAG, RESET_ALT, "Reset")
a_Noclean=		cli.AddArg(NOCLEAN_FLAG, NOCLEAN_ALT, "Noclean")
a_Fullclean=	cli.AddArg(FCLEAN_FLAG, FCLEAN_ALT, "Fullclean")
a_Nobuild=		cli.AddArg(NBUILD_FLAG, NBUILD_ALT, "Nobuild")
a_Help=			cli.AddExclusiveArg(HELP_FLAG, HELP_ALT, "Help")
a_Version=		cli.AddExclusiveArg(VERSION_FLAG, VERSION_ALT, "Version")

cli.AddGroup(Conflict.Error, a_Skip, a_Force)
cli.AddGroup(Conflict.Error, a_Skip, a_Reset)
cli.AddGroup(Conflict.Error, a_Fullclean, a_Noclean)
cli.AddGroup(Conflict.Overlap, a_Reset, a_Fullclean)
cli.AddGroup(Conflict.Overlap, a_Reset, a_Force)

args = cli.Parse(argv)

if ("Help" in args and args["Help"]):
	print(Usage)
	exit(code=0)

if ("Version" in args and args["Version"]):
	print(f"{C_EMPHASIS}Using {SDK_NAME} version {Colors.Yellow}{SDK_VERSION}{C_EMPHASIS} by worseuserr.{Colors.Reset}")
	exit(code=0)

isFirstLaunch = not os.path.exists(join(".", SETUP_FILE))
shouldSetup = (args["Force"] or args["Reset"]) or (isFirstLaunch and not args["Skip"])

if (args["Verbose"]):
	Output.LogLevel = "verbose"
else:
	Output.LogLevel = config["LogLevel"]

if (args["Reset"]):
	args["Fullclean"] = True

# BUILD

Output.Write(f"{C_EMPHASIS}Started build using SDK version {SDK_VERSION}\n")

if (args["Fullclean"]):
	args["Noclean"] = False
	Output.Write(f"{C_PRIMARY}Performing full clean...\n")
	Shell.ClearDir(join(".", BUILD))
	Output.Write(f"{C_PRIMARY}/{BUILD} cleared.\n")
	Shell.SafeClearDir(join(".", LIB))
	Output.Write(f"{C_PRIMARY}/{LIB} cleared.\n")
	if (os.path.exists(join(".", SETUP_FILE))):
		os.remove(join(".", SETUP_FILE))
		Output.Write(f"{C_PRIMARY}Removed setup marker.\n")
if (not args["Noclean"]):
	Build.Cleanup(config)
if (args["Fullclean"] and not args["Reset"]):
	Output.Write(f"{C_EMPHASIS}Full clean completed.\n")
	exit(code=0)

if (shouldSetup):
	Build.Setup(config)
else:
	Build.CheckMissingDependencies(config)

sources = Build.GetSources(config)
if (args["Nobuild"]):
	exit(code=0)
Build.Build(sources)
