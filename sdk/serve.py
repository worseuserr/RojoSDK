import subprocess

try:
	subprocess.run(["rojo", "serve", "build.project.json"])
except:
	pass
