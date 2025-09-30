from tools.Constants import BUILD, LIB
from tools.Output import Colors

Usage = f"""
{Colors.White}Usage:{Colors.Reset} python3 build.py {Colors.Italic}[OPTIONS]{Colors.Reset}

{Colors.White}Description:{Colors.Reset}
   This script builds all your libraries with your source code into /{BUILD}.

{Colors.White}Options:{Colors.Yellow}
   -V, --version       Show the version and exit
   -h, --help          Show this message and exit
   -s, --skip-setup    Skip first-build setup (only use if you know what you are doing)
   -f, --force-setup   Force first-build setup to run before building
   -v, --verbose       Enable more verbose output
   -r, --reset         Full clean and rerun setup
   -n, --no-clean      Disable automatically cleaning missing/trailing files and git entries
   -F, --full-clean    Clean everything, including {BUILD} and {LIB} folders (destructive){Colors.Reset}"""
