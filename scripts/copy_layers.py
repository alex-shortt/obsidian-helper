import sys, os
import shutil, errno

basis_path = "/Users/alex/worlds/basis/basis-language"
muse_path = "/Users/alex/worlds/muse/muse-stories"

def copy_anything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise

def main():
	shutil.rmtree(muse_path + "/1_metaphysics")
	shutil.rmtree(muse_path + "/2_basis")
	copy_anything(basis_path + "/1_metaphysics", muse_path + "/1_metaphysics")
	copy_anything(basis_path + "/2_basis", muse_path + "/2_basis")

if __name__ == '__main__':
	sys.exit(main())
