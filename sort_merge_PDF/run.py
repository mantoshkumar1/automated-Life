import argparse, sys, os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sort_merge_PDF.app.pdf_sorter_merger import PDFSorterMerger
from utility.user_input_functions import get_clean_user_input_paths, get_clean_user_output_path


def run_app():
    parser = argparse.ArgumentParser(description='Sort and merge PDF files.')
    parser.add_argument("--input-paths", type=str, required=True,
                        help="Full path of source directories (separated by comma) where PDFs are stored")
    parser.add_argument("--dest-dir", type=str, default='',
                        help="Optional destination directory path to store the merged PDF. Default=In source directories only")
    parser.add_argument("--target-pdf-size", type=int, default=0, help="Optional: Enter target size in MB for each merged PDF")

    args = parser.parse_args()
    target_pdf_size = args.target_pdf_size

    # Clean user-inputs, don't blindly trust user.
    input_dir_list = get_clean_user_input_paths(user_input=args.input_paths)  # list of str
    dest_dir = get_clean_user_output_path(user_input=args.dest_dir)  # str

    # Sample Run
    # input_dir = r'C:\Users\Username\Downloads\test'
    # dest_dir = ''

    img_to_pdf = PDFSorterMerger(user_input=input_dir_list, user_dest_path=dest_dir, target_pdf_size=target_pdf_size)
    img_to_pdf.process_user_request()


if __name__ == "__main__":
    run_app()
