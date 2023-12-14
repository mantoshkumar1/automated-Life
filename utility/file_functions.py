import os
import re
import traceback
from utility.logger_util.setup_logger import logger


def list_all_entries(directory: str) -> list:
    """List all the files and directories inside a directory"""
    try:
        entries = os.listdir(directory)
        entries = [os.path.join(directory, entry) for entry in entries]
        return entries  # list of absolute paths
    except Exception as e:
        logger.error(f"list_all_entries: exception occurred: {e}")
        logger.error(traceback.format_exc())
        return []


def list_files(directory: str, file_extensions: list = ['.pdf']) -> list:
    """Only return the list of files, not directories

    Note that file names are not modified in either lower or upper case.
    It is returned by this function as it is. But while checking the extension, this
    function does case-insensitive checking.

    @:param directory: Absolute path of a directory
    @:param file_extensions: <list of str> choose kind of file types you want to filter.
        If this is set to None or empty list, then no filtering based on file
        extensions will be performed.
    """
    try:
        entries = list_all_entries(directory)
        files = [entry for entry in entries if os.path.isfile(entry)]

        if file_extensions:
            # case-insensitive extension verification is going on
            files = [ff for ff in files if has_file_extension(ff, file_extensions)]

        return files

    except Exception as e:
        logger.error(f"list_files: exception occurred: {e}")
        logger.error(traceback.format_exc())
        return []


def list_directories(directory: str) -> list:
    """Only return the list of directories, not files"""
    try:
        entries = list_all_entries(directory)
        directories = [entry for entry in entries if os.path.isdir(entry)]
        return directories
    except Exception as e:
        logger.error(f"list_directories: exception occurred: {e}")
        logger.error(traceback.format_exc())
        return []


def is_directory(path: str) -> bool:
    """
    :param path: absolute path
    :return: Returns True if the specified path exists and is a directory, and
             False otherwise.
    """
    return os.path.isdir(path)


def create_directory(directory: str, force: bool = True) -> bool:
    """
    :param directory: absolute directory path
    :param force: if path doesn't exist then create one.
    :return:
    """
    try:
        os.makedirs(directory, exist_ok=force)
        return True
    except Exception as e:
        logger.error(f"create_directory: exception occurred: {e}")
        logger.error(traceback.format_exc())
        return False


def remove_directory(directory: str):
    try:
        os.rmdir(directory)
        return True
    except Exception as e:
        logger.error(f"remove_directory: exception occurred: {e}")
        logger.error(traceback.format_exc())
        return False


#
# File Related Operations Starts Here
def file_info(file_path: str) -> dict:
    """

    :param file_path: absolute path
    :return:
    """
    try:
        info_dict = {
            'size_in_bytes': os.path.getsize(file_path),  # To convert it MB, divide by (1024 * 1024)
            'last_modified': os.path.getmtime(file_path),
            'is_directory': os.path.isdir(file_path)
        }
        return info_dict
    except FileNotFoundError:
        logger.error(f"file_info: Path '{file_path}' not found")
        raise
    except PermissionError:
        logger.error(f"file_info: Permission error while accessing file {file_path}")
        raise
    except Exception as e:
        logger.error(f"file_info: exception occurred: {e}")
        raise e


def get_file_size_in_bytes(file_path):
    """Returns file size in bytes
    1 MB = bytes
    1 KB =
    1 k... find all other sizes and write here.
    """
    file_size_bytes = os.path.getsize(file_path)
    return file_size_bytes


def get_file_size_in_mb(file_path):
    """Returns file size in MB"""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    return file_size_mb


def is_file(path, file_extension='.pdf') -> bool:
    """
    Returns True if given input path represents a matching extension (default: PDF);
    returns False for directories.

    Raises FileNotFoundError for Non-existent file/folder path.

    :param path: str
    :param file_extension: str
    :return: bool
    """
    file_extension = file_extension.lower()

    if os.path.isfile(path):
        if not file_extension:
            return True
        if path.lower().endswith(file_extension):
            return True

    # must be directory or file with non-expected extension
    return False


def get_file_extension(file_path: str):
    """
    This function is used to get the extension of a file.
    Note that if you pass a directory path to this function then it returns extension=""

    Example:
      # >>> os.path.splitext(r"C:/Users/Downloads")
      # ("C://Users//Downloads", "")  <== notice empty string ["" in 'str' means True]

    :param file_path: r"C:/Users/Downloads/sample.csv"  # absolute path
    :return: ('.csv', "C:/Users/Downloads/sample")
    """
    try:
        base_name, extension = os.path.splitext(file_path)

        # Note, if file_path = directory or a filename without extension,
        # then this function return an empty string. This could lead to bug
        # in the application as >>> '' in 'string' returns True (false positive case).
        # This corner case needs to be handled in the calling function itself.
        # I don't think it will be appropriate to handle here.

        return extension, base_name  # To user: be careful when extension = ''

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
        return '', ''


def has_file_extension(file_path: str, target_extensions=['.pdf']) -> bool:
    """
    This function extracts the actual file extension from the file path and performs
    a case-insensitive comparison with the provided target extension.

    :param file_path:
    :param target_extensions: list of str
    :return: If the file has one of the specified extensions, the function returns True;
            otherwise, it returns False.
    """
    file_extension, _ = get_file_extension(file_path)  # '.pdf'
    if not file_extension:  # empty str (either directory or filename without extension)
        return False

    target_extensions = [ext.lower() for ext in target_extensions]
    return file_extension.lower() in target_extensions


def get_file_name(file_path: str) -> str:
    """
    :param file_path: "/path/to/your/directory/your_file.txt"
    :return: your_file.txt
    """
    try:
        return os.path.basename(file_path)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
        return ''


def get_directory_name(file_path: str) -> str:
    """
    :param file_path: "/path/to/your/directory/your_file.txt"
    :return: /path/to/your/directory
    """
    try:
        return os.path.dirname(file_path)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
        return ''


def get_unique_filepath_in_same_dir(file_path: str) -> str:
    """
    If a file does not exist at given path, then simply return the same file path.

    If a file already exists then Get a unique file name in the same directory by
    appending a counter to the original file name.

    It is user responsibility to provide valid file_path.

    :param file_path: "/path/to/your/directory/your_file.txt" (absolute path)
    :return: a path similar to input file_path but that doesn't exist.
    """
    file_extension, base_name = get_file_extension(file_path)
    unique_file_path = file_path

    # Initialize a counter for appending to the file name
    counter = 0

    # Generate a new file name by appending a counter until a unique name is found
    while True:
        if not os.path.exists(unique_file_path):
            return unique_file_path

        counter += 1
        unique_file_path = f"{base_name}_dup_{counter}{file_extension}"


def sort_filenames_numerically(filenames):
    """
    Sort a list of filenames containing numbers in numerical order rather than
    lexicographical order. It extracts the numeric part of each filename and
    sorts based on these numeric values.

    Parameters:
    - filenames (list of str): List of filenames to be sorted.

    Returns:
    - list of str: Sorted list of filenames in numerical order.

    Example:
        Input: ['page-1.jpg', 'page-10.jpg', 'page-2.jpg']
        Output: ['page-1.jpg', 'page-2.jpg', 'page-10.jpg']
    """
    # todo: make it like Windows. If you say filenames = ['IMG_0001-page-1.jpg', 'IMG_0001-page-2.jpg', 'IMG_0001-page-10.jpg'] then it fails.
    #  In this case, it returns ['IMG_0001-page-1.jpg', 'IMG_0001-page-10.jpg', 'IMG_0001-page-2.jpg'].
    #   It should have still returned ['IMG_0001-page-1.jpg', 'IMG_0001-page-2.jpg', 'IMG_0001-page-10.jpg'] But doesn't.
    return sorted(filenames, key=lambda f: int(re.findall(r'\d+', f)[0]))

#
# File Related Operations End Here
