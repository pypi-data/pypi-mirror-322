import os
import stat
import time
from datetime import datetime

def get_file_attributes(file_path):
    """
    Retrieves all attributes of a file and returns them in dictionary form.

    Args:
    file_path (str): The path to the file.

    Returns:
    dict: A dictionary containing the file's attributes.
    """
    file_attributes = {}

    # File existence and type
    file_attributes['exists'] = os.path.exists(file_path)
    file_attributes['is_file'] = os.path.isfile(file_path)
    file_attributes['is_dir'] = os.path.isdir(file_path)

    # File permissions
    if file_attributes['exists']:
        file_stat = os.stat(file_path)
        file_attributes['permissions'] = stat.filemode(file_stat.st_mode)
        file_attributes['owner_id'] = file_stat.st_uid
        file_attributes['group_id'] = file_stat.st_gid

    # File size and disk usage
    if file_attributes['is_file']:
        file_attributes['size'] = os.path.getsize(file_path)
        file_attributes['size_human_readable'] = convert_size(os.path.getsize(file_path))

    # File timestamps
    if file_attributes['exists']:
        file_stat = os.stat(file_path)
        file_attributes['created_at'] = datetime.fromtimestamp(file_stat.st_ctime)
        file_attributes['modified_at'] = datetime.fromtimestamp(file_stat.st_mtime)
        file_attributes['accessed_at'] = datetime.fromtimestamp(file_stat.st_atime)

    # File name and path
    file_attributes['name'] = os.path.basename(file_path)
    file_attributes['path'] = file_path
    file_attributes['absolute_path'] = os.path.abspath(file_path)
    file_attributes['directory'] = os.path.dirname(file_path)

    return file_attributes

def convert_size(size):
    """
    Converts a size in bytes to a human-readable format.

    Тест

    Args:
    size (int): The size in bytes.

    Returns:
    str: The size in a human-readable format.
    """
    for unit in ['', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

# Example usage
"""
if __name__ == '__main__':
    file_path = input("Enter the file path: ")
    file_attributes = get_file_attributes(file_path)
    for attribute, value in file_attributes.items():
        print(f"{attribute}: {value}")
"""
