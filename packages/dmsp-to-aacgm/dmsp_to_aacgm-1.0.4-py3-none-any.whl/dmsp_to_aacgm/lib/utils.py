from typing import List
import os


def get_files(path: str) -> List[str]:
    """
    Takes a file path or directory path and returns a list of files.
    If the path refers to a file, returns a list with that file.
    If the path refers to a directory, returns a list of files within that directory (non-recursive).

    Args:
        path (str): The file or directory path.

    Returns:
        List[str]: A list of file paths.
    """
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return []


def build_output_path(file_path: str, output_dir: str) -> str:
    """
    Constructs a new file path using the specified output directory and the filename of the original file path.

    Args:
        file_path (str): The original file path.
        output_dir (str): The directory where the new file path should reside.

    Returns:
        str: The new file path in the output directory.
    """
    filename = os.path.basename(file_path)
    return os.path.join(output_dir, filename)
    