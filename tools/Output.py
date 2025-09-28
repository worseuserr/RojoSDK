from datetime import datetime
import sys

class Colors:
	# Text colors
	Black	= "\033[30m"
	Red		= "\033[31m"
	Green	= "\033[32m"
	Yellow	= "\033[33m"
	Blue	= "\033[34m"
	Magenta	= "\033[35m"
	Cyan	= "\033[36m"
	White	= "\033[37m"
	Reset	= "\033[0m"

	# Bright text colors
	BrightBlack	= "\033[90m"
	BrightRed	= "\033[91m"
	BrightGreen	= "\033[92m"
	BrightYellow= "\033[93m"
	BrightBlue	= "\033[94m"
	BrightMagenta= "\033[95m"
	BrightCyan	= "\033[96m"
	BrightWhite	= "\033[97m"

	# Background colors
	BgBlack		= "\033[40m"
	BgRed		= "\033[41m"
	BgGreen		= "\033[42m"
	BgYellow	= "\033[43m"
	BgBlue		= "\033[44m"
	BgMagenta	= "\033[45m"
	BgCyan		= "\033[46m"
	BgWhite		= "\033[47m"

	# Bright background colors
	BgBrightBlack	= "\033[100m"
	BgBrightRed		= "\033[101m"
	BgBrightGreen	= "\033[102m"
	BgBrightYellow	= "\033[103m"
	BgBrightBlue	= "\033[104m"
	BgBrightMagenta	= "\033[105m"
	BgBrightCyan	= "\033[106m"
	BgBrightWhite	= "\033[107m"

class Output:
	LogLevel = "normal"

	def WriteInPlace(str):
		sys.stdout.write("\r")
		Output.Write(("\n" if (Output.LogLevel == "verbose") else "") + f"{str}")

	def Write(str):
		if (Output.LogLevel == "quiet"):
			return
		append = f"{Colors.Yellow}[" + datetime.now().strftime("%H:%M:%S.%f")[:-3] + f"] {Colors.Reset}"
		if (Output.LogLevel == "verbose"):
			if (len(str) > 0 and str[0] == '\n'):
				str = str[1:]
				append = "\n" + append
		sys.stdout.write(append + str + Colors.Reset)
		sys.stdout.flush()

	def LoadingBar(segments, total, progress, append = ""):
		symbol = "="
		greenSegments = int(segments * (progress / total))
		redSegments = segments - greenSegments

		bar = Colors.Green + symbol * greenSegments + Colors.Red + symbol * redSegments + Colors.Reset
		Output.WriteInPlace(f"{Colors.Red}[{bar}{Colors.Red}]{Colors.Reset}{append}")