import os
from utility import file_functions


def is_pdf_or_directory(file_path: str) -> bool:
    """The function returns True because it's either a PDF file or a regular file.
    Otherwise, it returns False."""
    return os.path.isdir(file_path) or (
            os.path.isfile(file_path) and file_path.lower().endswith('.pdf'))


def is_pdf(file_path: str) -> bool:
    """Return True if file_path is a PDF file; else return False
    @:param file_path: absolute path
    @:returns: bool
    """
    return file_functions.is_file(path=file_path, file_extension='.pdf')

