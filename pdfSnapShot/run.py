import argparse
from typing import List

from pdfSnapShot.app.pdf_snapshot import PDFSnapshotGenerator
from utility.logger_util.setup_logger import logger


def generate_snapshots_of_pdf_pages(user_input: List[str], dest_path: str, image_quality: int):
    """
    Generate JPEG snapshots of each page of the PDF files in the input directories/pdfs.
    :param user_input: (list) A list of user items.
    :param dest_path: (str) The optional destination directory to store generated images
    :param image_quality: (int) Quality percentage of generated images
    :return:
    """
    generator = PDFSnapshotGenerator(user_input=user_input, user_dest_path=dest_path, quality=image_quality)
    generator.generate_pdf_snapshots()  # Generate snapshots from PDF pages
    logger.info("PDF snapshots generation completed.")


def get_clean_user_input(user_input: str) -> List[str]:
    """
    Clean the user data and strip unnecessary information from each item in the list.
    Please note that the function assumes that the user input is separated by comma.
    :param user_input: user input separated by comma, example: "C:\Documents\, D:\Receipts\"
    :return: list <str>, example: ["C:\Documents\", "D:\Receipts\"]
    """
    user_input = user_input.strip().split(",")  # user input separated by comma

    cleaned_user_input = []
    for user_item in user_input:
        # Strip leading/trailing whitespace and remove any unwanted characters
        cleaned_user_item = user_item.strip().replace("\n", "").replace("\r", "")
        if cleaned_user_item:
            cleaned_user_input.append(cleaned_user_item)

    # Use the cleaned list of user input for further processing
    # cleaned_user_input contains the user input with unnecessary info stripped
    return cleaned_user_input


def run_app():
    parser = argparse.ArgumentParser(description="PDF Snapshot Generator")
    parser.add_argument("--input-paths", type=str, help="Paths to the input PDFs or directories separated by commas", required=True)
    parser.add_argument("--dest-path", type=str, help="Optional destination directory path to store the generated images", default='')
    parser.add_argument("--quality", type=int, help="Optional: Enter quality reduction percentage of generated images", default=20)
    args = parser.parse_args()

    # Clean user-input, don't blindly trust user.
    input_paths = get_clean_user_input(user_input=args.input_paths)
    dest_path = args.dest_path.strip().replace("\n", "").replace("\r", "")
    image_quality = args.quality

    # Generate the Snapshot of all PDF files
    generate_snapshots_of_pdf_pages(user_input=input_paths, dest_path=dest_path, image_quality=image_quality)


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
#     generate_snapshots_of_pdf_pages(pdfs_source_directory_paths)
#
