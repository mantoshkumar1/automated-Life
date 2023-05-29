import argparse
from typing import List

from PDFSnapShot.app.pdf_snapshot import PDFSnapshotGenerator
from utility.logger_util.setup_logger import logger


def generate_snapshots_of_pdf_pages(input_directories: List[str]):
    """
    Generate JPEG snapshots of each page of the PDF files in the input directories.
    :param input_directories (list): A list of input directories where the PDF files are located.
    :return:
    """
    generator = PDFSnapshotGenerator(input_directories=input_directories)
    generator.generate_snapshots()  # Generate snapshots from PDF pages
    logger.info("PDF snapshots generation completed.")


def get_clean_user_input(user_input: str) -> List[str]:
    """
    Clean the user data and strip unnecessary information from each item in the list.
    Please note that the function assumes that the user input is separated by comma.
    :param user_input: user input separated by comma, example: "C:\Documents\, D:\Receipts\"
    :return: list <str>, example: ["C:\Documents\", "D:\Receipts\"]
    """
    input_directories = user_input.strip().split(",")  # user input separated by comma

    cleaned_directories = []
    for directory in input_directories:
        # Strip leading/trailing whitespace and remove any unwanted characters
        cleaned_directory = directory.strip().replace("\n", "").replace("\r", "")
        if cleaned_directory:
            cleaned_directories.append(cleaned_directory)

    # Use the cleaned list of directories for further processing
    # cleaned_directories contains the user input with unnecessary info stripped
    return cleaned_directories


def run_app():
    parser = argparse.ArgumentParser(description="PDF Snapshot Generator")
    parser.add_argument("--input_dirs", type=str, help="Paths to the input directories containing PDF files, separated by commas")
    args = parser.parse_args()

    if args.input_dirs:
        input_directories = get_clean_user_input(user_input=args.input_dirs)  # don't trust user
        generate_snapshots_of_pdf_pages(input_directories=input_directories)
    else:
        logger.error("Please provide the --input_dirs argument with paths to the input "
                     "directories separated by commas.")


if __name__ == "__main__":
    run_app()


# If you ever want to use this application programmatically, use the below code:
#
# if __name__ == "__main__":
#     # Provide the input/output directory of PDF files
#     pdfs_source_directory_paths = [
#         r'C:\Users\MANTKUMAR\Documents\mantosh-backup\',
#     ]
#
#     # Generate snapshots from PDF pages
#     generate_snapshots_of_pdf_pages(input_directories=pdfs_source_directory_paths)
#
