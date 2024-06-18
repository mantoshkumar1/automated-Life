from utility import file_functions

# Add more image extensions as needed (add in lower-case only; follow a pattern)
global_image_extensions = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".heic", ".webp", ".ico", ".svg",
    ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".ppm", ".pgm", ".pbm", ".hdr", ".pic",
    ".psd", ".cdr", ".wmf", ".emf"}

# making sure global_image_extensions are uniform in lower-case for easy comparisons.
global_image_extensions = {ext.lower() for ext in global_image_extensions}


def list_image_files(directory: str) -> list:
    """List all image file paths in a specified directory"""
    # image_only_files = list_files(directory, global_image_extensions)
    image_only_files = file_functions.list_files(directory, global_image_extensions)
    return image_only_files


def is_image_file(file_path: str) -> bool:
    """Return True if file has one of the image extensions mentioned in the global
    variable 'global_image_extensions'.

    Note that if file_path is a directory or does not have an extension, then this
    function returns False.

    :param file_path: absolute path of file
    :return: True / False
    """
    file_extension, _ = file_functions.get_file_extension(file_path)
    if not file_extension:  # empty str (either directory or filename without extension)
        return False

    return file_extension.lower() in global_image_extensions
