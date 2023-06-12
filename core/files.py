""" This module contains functions to manage files not
exactly associated with notty repository's directory. """

from fnmatch import fnmatch
from typing import Sequence
import shutil
import stat
import os

from core.path import Path


def remove_current(path: Path) -> None:
    """ Remove current code from project's directory. """
    bin_path = path // ".notty" // "bin"
    for top_file in os.listdir(str(path)):
        if "notty" in top_file:
            continue

        full_path = path / top_file
        shutil.move(str(full_path), str(bin_path))
        moved_file = bin_path / top_file
        
        if moved_file.is_dir():
            os.chmod(str(moved_file/""), stat.S_IWRITE)
            shutil.rmtree(str(moved_file))
        else:
            os.remove(str(moved_file))

def name_in_patterns(file_name: str, patterns: Sequence[str]) -> bool:
    """ Check if given file_name matches any pattern from 
    patterns using fnmatch checker function. """
    for pattern in patterns:
        if fnmatch(file_name, pattern):
            return True
    return False
