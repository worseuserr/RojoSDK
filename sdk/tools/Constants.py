import os
from tools.Output import Colors

SDK_NAME=		"RojoSDK"
SDK_VERSION=	"1.4.0"
SDK_SCRIPT=		"build.py"

BUILD=			"build"
SOURCE=			"src"
LIB=			"lib"
TMP=			"tmp"
CONFIG_FILE=	"build.config.toml"
SETUP_FILE=		os.path.normpath("tools/.setupmarker.txt")
UPDATE_FILE=	os.path.normpath("tools/.lastupdate.txt")

SKIP_FLAG=		"--skip-setup"
SKIP_ALT=		"-s"
FORCE_FLAG=		"--force-setup"
FORCE_ALT=		"-f"
VERBOSE_FLAG=	"--verbose"
VERBOSE_ALT=	"-v"
RESET_FLAG=		"--reset"
RESET_ALT=		"-r"
NOCLEAN_FLAG=	"--no-clean"
NOCLEAN_ALT=	"-N"
FCLEAN_FLAG=	"--full-clean"
FCLEAN_ALT=		"-F"
NBUILD_FLAG=	"--no-build"
NBUILD_ALT=		"-n"
HELP_FLAG=		"--help"
HELP_ALT=		"-h"
VERSION_FLAG=	"--version"
VERSION_ALT=	"-V"

C_EMPHASIS=		Colors.White
C_PRIMARY=		Colors.Reset
C_GOOD=			Colors.Green
C_WARN=			Colors.Yellow
C_BAD=			Colors.Red

# Filenames to ignore when checking collisions during build (only first instance is used)
ALLOWED_DUPLICATES=	["init.meta.json"]

# Only for SDK debugging, this will delete lib/ on setup
DEBUG_DELETE_LIB=	False
