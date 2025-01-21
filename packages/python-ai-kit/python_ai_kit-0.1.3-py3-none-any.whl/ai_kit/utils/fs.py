"""Filesystem utilities for ai-kit."""
import os
import stat
from pathlib import Path

def remove_file(file_path: Path) -> None:
    """Remove a single file, changing permissions and retrying if needed."""
    try:
        file_path.unlink()
    except PermissionError:
        os.chmod(file_path, stat.S_IWRITE)
        file_path.unlink()
    except FileNotFoundError:
        pass

def remove_dir(dir_path: Path) -> None:
    """Remove a single directory, changing permissions and retrying if needed."""
    try:
        dir_path.rmdir()
    except PermissionError:
        os.chmod(dir_path, stat.S_IWRITE)
        dir_path.rmdir()
    except OSError as e:
        raise e

def remove_tree(root: Path) -> None:
    """Recursively remove a directory tree, handling read-only files/directories."""
    if not root.exists():
        return
    if not root.is_dir():
        raise ValueError(f"{root} is not a directory.")

    # Walk bottom-up
    for dirpath, dirnames, filenames in os.walk(str(root), topdown=False):
        # Remove files first
        for filename in filenames:
            file_path = Path(dirpath) / filename
            remove_file(file_path)

        # Then remove directories
        for dirname in dirnames:
            dir_path = Path(dirpath) / dirname
            remove_dir(dir_path)

    # Finally remove the root folder
    remove_dir(root) 