from tools.CLI import CLI, Conflict, ArgType

def Test():
	cli = CLI()
	q = cli.AddArg("--quiet", "-q", "Quiet")
	v = cli.AddArg("--verbose", "-v", "Verbose")
	f = cli.AddArg("--force", "-f", "Force")
	u = cli.AddArg("--unused", "-u", "Unused")
	fc = cli.AddArg("--fclean", "-F", "Fclean")
	r = cli.AddArg("--reset", "-r", "Reset")
	ver = cli.AddExclusiveArg("--version", "-V", "Version")

	# Add arguments with types other than Bool to test them
	name = cli.AddArg("--name", "-n", "Name", ArgType.String)
	count = cli.AddArg("--count", "-c", "Count", ArgType.Int)
	tags = cli.AddArg("--tags", "-t", "Tags", ArgType.StringArray)
	ids = cli.AddArg("--ids", "-i", "Ids", ArgType.IntArray)

	# Activate the error group and keep the overlap group
	cli.AddGroup(Conflict.Error, q, v)
	cli.AddGroup(Conflict.Overlap, fc, r)

	print("--- Basic Test Cases ---")
	result = cli.Parse(["test.py", "--force", "--reset", "-F"])
	print(f"Input: ['test.py', '--force', '--reset', '-F']\nResult: {result}\n")

	result = cli.Parse(["test.py", "--quiet", "--force", "-V", "--reset", "-F"])
	print(f"Input: ['test.py', '--quiet', '--force', '-V', '--reset', '-F']\nResult: {result}\n")

	result = cli.Parse(["test.py", "-V"])
	print(f"Input: ['test.py', '-V']\nResult: {result}\n")

	print("--- Testing Default Values ---")
	result = cli.Parse(["test.py"])
	print(f"Input: ['test.py']\nResult: {result}\n")

	print("--- Testing Argument Types ---")
	result = cli.Parse(["test.py", "--name", "my-project", "-c", "42", "--tags", "api,web, db", "-i", "101, 202,303"])
	print(f"Input: ['test.py', '--name', 'my-project', '-c', '42', '--tags', 'api,web, db', '-i', '101, 202,303']\nResult: {result}\n")

	print("--- Testing Conflict.Error Group ---")
	print("NOTE: This test should trigger an error and exit. The script will stop if it works correctly.")
	try:
		# This call should cause the program to exit with code 1.
		result = cli.Parse(["test.py", "--quiet", "-v"])
		print(f"FAILURE: Program continued. Result: {result}\n")
	except SystemExit as e:
		print(f"SUCCESS: Program exited as expected with code {e.code}.\n")

	print("--- Testing Error: Missing Parameter ---")
	print("NOTE: This test should trigger an error for a missing parameter.")
	try:
		result = cli.Parse(["test.py", "--name"])
		print(f"FAILURE: Program continued. Result: {result}\n")
	except SystemExit as e:
		print(f"SUCCESS: Program exited as expected with code {e.code}.\n")

	print("--- Testing Error: Invalid Integer Parameter ---")
	print("NOTE: This test should trigger an error for a bad integer value.")
	try:
		result = cli.Parse(["test.py", "--count", "not-a-number"])
		print(f"FAILURE: Program continued. Result: {result}\n")
	except SystemExit as e:
		print(f"SUCCESS: Program exited as expected with code {e.code}.\n")

	print("--- Testing Error: Invalid Integer in Array ---")
	print("NOTE: This test should trigger an error for a bad integer value in an array.")
	try:
		result = cli.Parse(["test.py", "--ids", "1,2,three,4"])
		print(f"FAILURE: Program continued. Result: {result}\n")
	except SystemExit as e:
		print(f"SUCCESS: Program exited as expected with code {e.code}.\n")

	print("--- Testing Error: Invalid Option ---")
	print("NOTE: This test should trigger an error for a non-existent flag.")
	try:
		result = cli.Parse(["test.py", "--non-existent-flag"])
		print(f"FAILURE: Program continued. Result: {result}\n")
	except SystemExit as e:
		print(f"SUCCESS: Program exited as expected with code {e.code}.\n")

