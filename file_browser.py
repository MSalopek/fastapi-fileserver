import os
from pathvalidate import is_valid_filename
from fastapi import FastAPI
import zipfile
from io import BytesIO


DEFAULT_BASE = "./data/"

def validate_filename(pathname: str) -> bool:
    """
    Validate the filename given by the user.
    Zero length names are invalid and so are names that start with a "/" or contain ".."
    """
    if not len(pathname) or pathname.find("..") != -1:
        return False

    return is_valid_filename(pathname)

def exists(base: str, pathname: str) -> bool:
    """
    Check if the file exists under the given base directory.
    """
    return os.path.exists(os.path.join(base, pathname))


def can_rename(from_name: str, to_name: str) -> bool:
    """
    Only files under the same directory can be renamed.
    """
    return os.path.dirname(from_name) == os.path.dirname(to_name)


def rename(base: str, from_name: str, to_name: str) -> bool:
    """
    Perform file rename under rules enforced by can_rename and validate_filename.
    If the rename operation fails, return False.
    """
    if not can_rename(from_name, to_name):
        return False

    if not validate_filename(to_name.split("/")[-1]):
        return False

    try:
        os.rename(
            os.path.join(base, from_name),
            os.path.join(base, to_name),
        )
    except:
        return False


def search_files(base, pattern):
    """
    Find all files matching the pattern argument starting from the base directory.
    * base dir path will be stripped from results
    """
    res = []
    for (p, _, files) in os.walk(base):
        for f in files:
            if f.find(pattern) != -1:
                res.append(os.path.join(p, f).replace(base, "", 1)) 
    return res


def zip_files(basepath: str, file_list: list[str]) -> BytesIO:
    """
    Takes a file_list, expands it and creates a zip file in memory
    returning a reference to the BytesIO object.
    """
    io_buffer = BytesIO()
    full_paths = [os.path.join(basepath, f) for f in file_list]
    with zipfile.ZipFile(io_buffer, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in full_paths:
            zip.write(fpath)
    return io_buffer
