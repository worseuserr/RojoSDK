from tools.CLI import CLI, Conflict

def Test():
	cli = CLI()
	q = cli.AddArg("--quiet", "-q", "Quiet")
	v = cli.AddArg("--verbose", "-v", "Verbose")
	f = cli.AddArg("--force", "-f", "Force")

	cli.AddGroup(Conflict.Error, q, v)

	result = cli.Parse("--quiet", "-v", "--force")
	print(result)
