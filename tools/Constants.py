from tools.Output import Colors

BUILD=			"build"
SOURCE=			"src"
LIB=			"lib"
CONFIG_FILE=	"build.config.toml"
SETUP_FILE=		"tools/.setupmarker.txt"
UPDATE_FILE=	"tools/.lastupdate.txt"
SKIP_FLAG=		"--skip-setup"
FORCE_FLAG=		"--force-setup"
VERBOSE_FLAG=	"--verbose"
SKIP_ALT=		"-s"
FORCE_ALT=		"-f"
VERBOSE_ALT=	"-v"

C_EMPHASIS=	Colors.White
C_PRIMARY=	Colors.Reset
C_GOOD=		Colors.Green
C_WARN=		Colors.Yellow
C_BAD=		Colors.Red

DEBUG_DELETE_LIB=	True
