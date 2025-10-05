from zipfile import ZipFile, ZIP_DEFLATED
from os.path import join
import os, shutil, stat

# Script for building the SDK into a releasable state.
# It will create all necessary empty folders and package everything
# into a zip file.

# BUILD is where you can freely test the built SDK.
# BIN is where the zip file is created.

BUILD=	"build"
BIN=	"bin"
NAME=	"RojoSDK-v.zip"
SDK=	"sdk"
SDKMETA=".sdk"
FOLDERS_TO_CREATE=	["lib", "src", "build", SDKMETA]
FILES_TO_SDKMETA=	["LICENSE", "README.md"]

# From tools.Shell
class Shell:
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

if (not os.path.isdir(build)):
	os.mkdir(build)
if (not os.path.isdir(bin)):
	os.mkdir(bin)

Shell.ClearDir(build)
Shell.ClearDir(bin)
Shell.CopyDir(join(".", SDK), build)

for path in FOLDERS_TO_CREATE:
	if (os.path.isdir(join(build, path))):
		continue
	os.mkdir(join(build, path))

for file in FILES_TO_SDKMETA:
	if (os.path.isfile(join(build, SDKMETA, file))):
		continue
	shutil.copy2(join(".", file), join(build, SDKMETA, file))

# Create zip file
with ZipFile(output, 'w', compression=ZIP_DEFLATED) as zf:
	for root, _, files in os.walk(build):
		for file in files:
			file_path = os.path.join(root, file)
			arcname = os.path.relpath(file_path, output)
			zf.write(file_path, arcname)
