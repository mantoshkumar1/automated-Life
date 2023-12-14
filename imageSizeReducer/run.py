from PIL import Image
import os
import pathlib
from typing import List

from utility.logger_util.setup_logger import logger






# Example usage
# input_path = 'path/to/your/image.jpg'
# input_path = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\document bank\manisha docs\manisha last 4 months bank statements\chequing account\pdf-snapshots\New folder\chequing-april-2023-page-1.jpg'
input_path = r'C:\Users\MANTKUMAR\Downloads\experiments'
reduction_percentage = 20  # Reduce file size by 20%

output_path = reduce_image_file_size(input_path, reduction_percentage)
if output_path:
    print(f"Compressed image saved at: {output_path}")
else:
    print("Failed to compress image within the specified reduction percentage.")





##########################3


import argparse
from imageSizeReducer.app.reduce_image_size import ImageSizeReducer
from utility.user_input_functions import get_clean_user_input_paths, get_clean_user_output_path


def run_app():
    parser = argparse.ArgumentParser(description="PDF Compressor")
    parser.add_argument("--input-paths", type=str, help="Paths to the input PDFs or directories separated by commas", required=True)
    parser.add_argument("--dest-dir", type=str, help="Optional destination directory path to store the compressed PDF", default='')
    parser.add_argument("--target-pdf-size", type=int, help="Optional: Enter target size in MB for each compressed PDF", required=True)
    args = parser.parse_args()

    # todo (02 Mar 2024): May be add an attribute 'memory_unit' and provide options
    #  for 'MB' and 'KB'. By default, make it MB. Currently app assumes value provided
    #  in 'target-pdf-size' is in MB. Since this argument works best if input is int so
    #  those files which are in KB cannot used this application. Think about them.

    # Clean user-inputs, don't blindly trust user.
    input_dirs = get_clean_user_input_paths(user_input=args.input_paths)  # list of str
    dest_dir = get_clean_user_output_path(user_input=args.dest_dir)  # str

    target_pdf_size = args.target_pdf_size

    # Sample Run
    # input_dirs = [r'C:\\Users\\MANTOSH\\Downloads', r'C:\\Users\\MANTOSH\\Downloads\\sample.pdf']
    # dest_dir = r'C:\Users\MANTOSH\Downloads\del'
    # target_pdf_size = 2 # in MB

    # pdf_compressor = PDFCompressor(user_input=input_dirs, user_dest_dir=dest_dir, target_pdf_size=target_pdf_size)
    # pdf_compressor.process_user_request()

    aa = ImageSizeReducer(user_input=[r'C:\Users\MANTKUMAR\Downloads\experiments\mk'],
                          user_dest_path=r'C:\Users\MANTKUMAR\Downloads\experiments\output')
    aa.process_user_request()


if __name__ == "__main__":
    run_app()
