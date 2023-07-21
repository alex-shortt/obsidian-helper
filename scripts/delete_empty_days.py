import sys, os
import shutil, errno
from pathlib import Path

basis_path = "/Users/alex/worlds/basis/basis-language/"
muse_path = "/Users/alex/worlds/muse/muse-stories/"

for path in Path(muse_path).rglob('daily/*.md'):
	with open(path, 'r+') as file:
		text = file.read()
		if text.strip() == "-":
			print(str(path) + " is empty")
			os.remove(path)
