import argparse
from typing import List
from compressPDF.app.pdf_compressor import PDFCompressor


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
    parser = argparse.ArgumentParser(description="PDF Compressor")
    parser.add_argument("--input-dirs", type=str, help="Paths to the input PDFs or directories separated by commas", required=True)
    parser.add_argument("--dest-dir", type=str, help="Optional destination directory path to store the compressed PDF", default='')
    parser.add_argument("--target-pdf-size", type=int, help="Optional: Enter target size in MB for each compressed PDF", required=True)
    args = parser.parse_args()

    # Clean user-input, don't blindly trust user.
    input_dirs = get_clean_user_input(user_input=args.input_dirs)
    dest_dir = args.dest_dir.strip().replace("\n", "").replace("\r", "")
    target_pdf_size = args.target_pdf_size

    # input_dirs = [r'C:\\Users\\MANTKUMAR\\Downloads\\delete']
    # dest_dir = r'C:\Users\MANTKUMAR\Downloads\del'
    # target_pdf_size = 2

    pdf_compressor = PDFCompressor(user_input=input_dirs, user_dest_dir=dest_dir, target_pdf_size=target_pdf_size)
    pdf_compressor.process_user_request()


if __name__ == "__main__":
    run_app()
