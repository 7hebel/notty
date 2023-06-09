from pathlib import Path
import shutil
import stat
import os

SKIP_ITEMS = [".git", "__pycache__", ".notty"]

def _contains(string: str, items) -> bool:
    string = string.casefold()

    for item in items:
        if item.casefold() in string:
            return True
    else:
        return False

def get_paths(path: Path | str, ignore_files: list[str] = [], ignore_dirs: list[str] = [".notty"]) -> list[Path]:
    if isinstance(path, str):
        path = str(Path(path).resolve(True))
    if isinstance(path, Path):
        path = str(path.resolve(True))

    subpaths = []

    for root, dirs, files in os.walk(str(path)):
        if _contains(root, SKIP_ITEMS):
            continue 

        for file in files:
            if not _contains(file, SKIP_ITEMS) and file not in ignore_files:
                fpath = root + "\\" + file
                subpaths.append(Path(fpath))

        for directory in dirs:
            if not _contains(directory, SKIP_ITEMS) and directory not in ignore_dirs:
                dpath = root + "\\" + directory
                subpaths.append(Path(dpath))

    return subpaths

def remove_current(path: str):
    bin_path = path + "/.notty/bin/"
    for top_file in os.listdir(path):
        if not "notty" in top_file:
            full_path = path + "/" + top_file

            shutil.move(full_path, bin_path)
            moved_file = bin_path+"/"+top_file

            if os.path.isdir(moved_file):
                os.chmod(bin_path+"/"+top_file+"/", stat.S_IWRITE)
                shutil.rmtree(moved_file)
            else:
                os.remove(bin_path+"/"+top_file)
