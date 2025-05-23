import os
from pathlib import Path
from agno.tools import tool
from typing import List, Optional
from agno.utils.log import log_debug, log_info, logger

default_ignore_dirs = [
    ".git", ".svn", ".hg",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".venv", "venv", "env", "build", "dist", ".tox", ".eggs",
    "node_modules", ".next", "out", "coverage", "lib",
    "vendor", "target", "bin",
    ".idea", ".vscode", ".DS_Store", "*.iml",
    "public", "static", "assets", "media", ".parcel-cache", ".turbo", ".storybook",
    ".docker", ".circleci", ".github", ".gitlab",
    "logs", "tmp", "temp", "__tests__", "test", ".cache", ".log", ".history"
]

@tool(
    name="get_dir_tree",
    description="Get the directory tree of a given base directory, excluding specified directories.",
)
def get_dir_tree(base_dir: str, ignore_dirs: Optional[List[str]] = None):
    """
    Get the directory tree of a given base directory, excluding specified directories.
    Args:
        base_dir (str): The base directory to start the search from.
        ignore_dirs (Optional[List[str]], optional): A list of directories to ignore.
    Returns:
        dict: A nested dictionary representing the directory tree.
    """
    ignore_set = set(default_ignore_dirs) | set(ignore_dirs or [])
    
    tree = {}

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ignore_set]

        rel_path = os.path.relpath(root, base_dir)
        
        if rel_path == ".":
            rel_path = ""

        parts = rel_path.split(os.sep) if rel_path else []
        current_level = tree
        for part in parts:
            current_level = current_level.setdefault(part, {})

        current_level["__files__"] = files

    return tree

def save_file(contents: str, file_name: str, overwrite: bool = True) -> str:
        """Saves the contents to a file called `file_name` and returns the file name if successful.

        :param contents: The contents to save.
        :param file_name: The name of the file to save to.
        :param overwrite: Overwrite the file if it already exists.
        :return: The file name if successful, otherwise returns an error message.
        """
        base_dir: Path = Path.cwd()
        try:
            file_path = base_dir.joinpath(file_name)
            log_debug(f"Saving contents to {file_path}")
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
            if file_path.exists() and not overwrite:
                return f"File {file_name} already exists"
            file_path.write_text(contents)
            log_info(f"Saved: {file_path}")
            return str(file_name)
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            return f"Error saving to file: {e}"