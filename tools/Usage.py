from tools.Output import Colors

Usage = f"""
{Colors.White}Usage:{Colors.Reset} python3 build.py {Colors.Italic}[OPTIONS]{Colors.Reset}

{Colors.White}Description:{Colors.Reset}
   This script builds all your libraries with your source code into /build.

{Colors.White}Options:{Colors.Yellow}
   -V, --version       Show the version and exit
   -h, --help          Show this message and exit
   -s, --skip-setup    Skip first-build setup (only use if you know what you are doing)
   -f, --force-setup   Force first-build setup to run before building
   -v, --verbose       Enable more verbose output
   -r, --reset         Clean everything and rerun setup
   -c, --clean         Clean everything and exit{Colors.Reset}"""
