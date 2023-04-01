# build_ark.py
from pathlib import Path
from subprocess import CalledProcessError
from sys import platform
import subprocess
from check_git_updated import check_git_updated

def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()

def make_executable_binaries():
    cmd_chmod_arkhelper = "chmod +x dependencies/linux/arkhelper".split()
    subprocess.check_output(cmd_chmod_arkhelper, shell=(platform == "win32"), cwd="..")
    cmd_chmod_dtab = "chmod +x dependencies/linux/dtab".split()
    subprocess.check_output(cmd_chmod_dtab, shell=(platform == "win32"), cwd="..")

# darwin: mac

def build_patch_ark():
    # directories used in this script
    print("Building Rock Band 2 Deluxe patch arks...")
    cwd = Path().absolute() # current working directory (dev_scripts)
    root_dir = cwd.parents[0] # root directory of the repo
    ark_dir = root_dir.joinpath("_ark")

    if platform == "win32":
        build_location = "_build\ps2\\gen"
    else:
        build_location = "_build/ps2/gen"
        # build the binaries if on linux/other OS
        if platform != "darwin":
            make_executable_binaries()
    patch_hdr_version = "MAIN"

    # pull the latest changes from the Rock Band 2 Deluxe repo if necessary
    if not check_git_updated(repo_url="https://github.com/hmxmilohax/rock-band-2-deluxe", repo_root_path=root_dir):
        cmd_pull = "git pull https://github.com/hmxmilohax/rock-band-2-deluxe ps2".split()
        subprocess.run(cmd_pull, shell=(platform == "win32"), cwd="..")

    # build the ark
    failed = False
    try:
        if platform == "win32":
            cmd_build = f"dependencies\windows\\arkhelper.exe dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 4 -s 4073741823".split()
        elif platform == "darwin":
            cmd_build = f"dependencies/macos/arkhelper dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 4 -s 4073741823".split()
        else:
            cmd_build = f"dependencies/linux/arkhelper dir2ark _ark {build_location} -n {patch_hdr_version} -e -v 4 -s 4073741823".split()
        subprocess.check_output(cmd_build, shell=(platform == "win32"), cwd="..")
    except CalledProcessError as e:
        print(e.output)
        failed = True

    if not failed:
        print("Successfully built Rock Band 2 Deluxe ARK.")
        return True
    else:
        print("Error building ARK. Check your modifications or run git_reset.py to rebase your repo.")
        return False