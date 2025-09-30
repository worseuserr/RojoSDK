from tools.Output import Colors

SDK_NAME=		"RojoSDK"
SDK_VERSION =	"1.0.0"

BUILD=			"build"
SOURCE=			"src"
LIB=			"lib"
CONFIG_FILE=	"build.config.toml"
SETUP_FILE=		"tools/.setupmarker.txt"
UPDATE_FILE=	"tools/.lastupdate.txt"

SKIP_FLAG=		"--skip-setup"
SKIP_ALT=		"-s"
FORCE_FLAG=		"--force-setup"
FORCE_ALT=		"-f"
VERBOSE_FLAG=	"--verbose"
VERBOSE_ALT=	"-v"
RESET_FLAG=		"--reset"
RESET_ALT=		"-r"
HELP_FLAG=		"--help"
HELP_ALT=		"-h"
VERSION_FLAG=	"--version"
VERSION_ALT=	"-V"
CLEAN_FLAG=		"--clean"
CLEAN_ALT=		"-c"

C_EMPHASIS=	Colors.White
C_PRIMARY=	Colors.Reset
C_GOOD=		Colors.Green
C_WARN=		Colors.Yellow
C_BAD=		Colors.Red

# Only for SDK debugging, this will /lib on setup
DEBUG_DELETE_LIB=	True
