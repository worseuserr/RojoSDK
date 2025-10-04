from tools.CLI import CLI, Conflict

def Test():
	cli = CLI()
	q = cli.AddArg("--quiet", "-q", "Quiet")
	v = cli.AddArg("--verbose", "-v", "Verbose")
	f = cli.AddArg("--force", "-f", "Force")
	u = cli.AddArg("--unused", "-u", "Unused")
	fc = cli.AddArg("--fclean", "-F", "Fclean")
	r = cli.AddArg("--reset", "-r", "Reset")
	ver = cli.AddExclusiveArg("--version", "-V", "Version")

	# cli.AddGroup(Conflict.Error, q, v)
	cli.AddGroup(Conflict.Overlap, fc, r)

	result = cli.Parse(["test.py", "--quiet", "-v", "--force", "--reset", "-F"])
	print(result)
	result = cli.Parse(["test.py", "--quiet", "-v", "--force", "-V", "--reset", "-F"])
	print(result)

