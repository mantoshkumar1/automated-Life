import argparse

from image2Pdf.app.merge_images_in_pdf import Image2PDF
from utility.user_input_functions import get_clean_user_input_paths, get_clean_user_output_path


def run_app():
    parser = argparse.ArgumentParser(description="Image 2 PDF")
    parser.add_argument("--input-path", type=str, help="Full path of source directory where images are strored", required=True)
    parser.add_argument("--dest-dir", type=str, help="Optional destination directory path to store PDF", default='')
    args = parser.parse_args()

    # Clean user-inputs, don't blindly trust user.
    input_dir = get_clean_user_input_paths(user_input=args.input_path)[0]  # list of str, only get first element
    dest_dir = get_clean_user_output_path(user_input=args.dest_dir)  # str

    # Sample Run
    # input_dir = r'C:\Users\Username\Downloads\test'
    # dest_dir = ''

    img_to_pdf = Image2PDF(user_input_dir=input_dir, user_dest_dir=dest_dir)
    img_to_pdf.process_user_request()


if __name__ == "__main__":
    run_app()
