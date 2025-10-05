from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from os.path import join
import os, shutil, stat, json, sys

# Script for building the SDK into a releasable state.
# It will create all necessary empty folders and package everything
# into a zip file.

# BUILD is where you can freely test the built SDK.
# BIN is where the zip file is created.

BUILD=		"build"
BIN=		"bin"
NAME=		"RojoSDK-v.zip"
SDK=		"sdk"
SRC=		"src"
SDKMETA=	".sdk"
PROJECTFILE="build.project.json"
FOLDERS_TO_CREATE=	["lib", "src", "build", SDKMETA]
FILES_TO_SDKMETA=	["LICENSE", "README.md"]

# From sdk.tools
class Shell:
	def Write(msg):
		append = f"\033[33m[" + datetime.now().strftime("%H:%M:%S.%f")[:-3] + f"] \033[0m"
		sys.stdout.write(append + str.replace(msg, '\t', "   ") + "\033[0m")
		sys.stdout.flush()

	def CopyDir(dir, target):
		if (not os.path.exists(target)):
			return
		for filename in os.listdir(dir):
			src = join(dir, filename)
			dst = join(target, filename)
			if os.path.isdir(src):
				shutil.copytree(src, dst, dirs_exist_ok=True)
			else:
				shutil.copy2(src, dst)

	def ClearDir(dir):
		if (not os.path.exists(dir)):
			return
		for filename in os.listdir(dir):
			if (filename == ".gitkeep"):
				continue
			path = join(dir, filename)
			if (os.path.isdir(path)):
				shutil.rmtree(path, onexc=Shell.RemoveReadonly)
			else:
				os.remove(path)

	def RemoveReadonly(func, path):
		os.chmod(path, stat.S_IWRITE)
		func(path)

build = join(".", BUILD)
bin = join(".", BIN)
sdkmeta = join(build, SDKMETA)
output = join(bin, NAME)

Shell.Write("Building SDK with vars:\n")
Shell.Write(f"\tbuild: {build}\n")
Shell.Write(f"\tbin: {bin}\n")
Shell.Write(f"\tsdkmeta: {sdkmeta}\n")
Shell.Write(f"\toutput: {output}\n")

if (not os.path.isdir(build)):
	os.mkdir(build)
if (not os.path.isdir(bin)):
	os.mkdir(bin)

Shell.Write(f"Clearing build...\n")
Shell.ClearDir(build)
Shell.Write(f"Clearing bin...\n")
Shell.ClearDir(bin)
Shell.Write(f"Copying SDK to build...\n")
Shell.CopyDir(join(".", SDK), build)
Shell.Write(f"Done.\n")

Shell.Write(f"Creating empty folders...\n")
for path in FOLDERS_TO_CREATE:
	if (os.path.isdir(join(build, path))):
		continue
	os.mkdir(join(build, path))

Shell.Write(f"Copying SDK meta files...\n")
for file in FILES_TO_SDKMETA:
	if (os.path.isfile(join(build, SDKMETA, file))):
		continue
	shutil.copy2(join(".", file), join(build, SDKMETA, file))

Shell.Write(f"Creating src folders...\n")
with open(join(".", SDK, PROJECTFILE)) as file:
	project = json.load(file)

for key, value in project["tree"].items():
	if (not isinstance(value, dict)):
		continue
	os.mkdir(join(build, SRC, key))
	for k, v in value.items():
		if (not isinstance(v, dict)):
			continue
		os.mkdir(join(build, SRC, key, k))
Shell.Write(f"Done.\n")

Shell.Write(f"Creating SDK zip...\n")
# Create zip file
with ZipFile(output, 'w', compression=ZIP_DEFLATED) as zf:
	for root, dirs, files in os.walk(build):
		# Add files
		for file in files:
			file_path = os.path.join(root, file)
			arcname = os.path.relpath(file_path, build)
			zf.write(file_path, arcname)
		# Add empty directories
		for dir in dirs:
			dir_path = os.path.join(root, dir)
			if (not os.listdir(dir_path)):
				arcname = os.path.relpath(dir_path, build) + '/'
				zf.writestr(arcname, '')
Shell.Write(f"Build completed. Output: {output}\n")
