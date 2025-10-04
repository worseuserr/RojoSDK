import os
import importlib.util

TEST_DIR = "tests"

for filename in os.listdir(TEST_DIR):
	if filename.endswith(".py"):
		filepath = os.path.join(TEST_DIR, filename)
		module_name = filename[:-3]  # Strip .py
		spec = importlib.util.spec_from_file_location(module_name, filepath)
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)
		if (hasattr(module, "Test")):
			print(f"Running Test() from {filename}")
			module.Test()
