import argparse
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from turnPdfBW.app.convert_pdf_blackwhite import PDFBlackWhiteConverter
from utility.user_input_functions import get_clean_user_input_paths, \
    get_clean_user_output_path


def run_app():
    parser = argparse.ArgumentParser(description="Convert PDFs into high-quality black-and-white versions")
    parser.add_argument("--input-paths", type=str,
                        help="Paths to the input PDFs or directories separated by commas",
                        required=True)

    parser.add_argument("--dest-path", type=str,
                        help="Optional destination directory path to store the generated images",
                        default='')

    parser.add_argument("--quality", type=int,
                        help="Optional: Enter quality of generated B&W PDFs in terms of percentage (max: 100)",
                        default=60)

    args = parser.parse_args()

    # Clean user-input, don't blindly trust user.
    input_paths = get_clean_user_input_paths(user_input=args.input_paths)  # list of str
    dest_path = get_clean_user_output_path(args.dest_path)  # str
    pdf_quality = int(args.quality)

    # Convert PDFs into high-quality black-and-white versions while preserving original files.
    PDFBlackWhiteConverter(
        user_input=input_paths, user_dest_path=dest_path, pdf_quality=pdf_quality
    ).convert_all_pdfs_to_BW()

if __name__ == "__main__":
    run_app()
