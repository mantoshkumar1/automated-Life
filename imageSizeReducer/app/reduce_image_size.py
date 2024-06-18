from PIL import Image
import os
from typing import List
import tempfile

from utility.logger_util.setup_logger import logger
from utility import file_functions
from utility import image_functions

"""
https://www.cic.gc.ca/english/helpcentre/answer.asp?qnum=1213
- Saving your images at a lower resolution, such as 96 DPI or 150 DPI, can greatly reduce image file size.

"""


class ImageSizeReducer:
    def __init__(self, user_input: List[str], user_dest_path: str = '', reduction_quality_percentage: int = 0, target_image_size: float = 0.0):
        self.user_input = user_input
        self.user_dest_path: str = user_dest_path

        self.reduction_quality_percentage = reduction_quality_percentage  # Quality of pic will be reduced by this %
        self.target_image_size = target_image_size  # in bytes

        # Warning: If user provides both 'reduction_quality_percentage' and
        # 'target_image_size' then 'target_image_size' will be chosen for processing.
        if self.target_image_size and self.reduction_quality_percentage:
            logger.info(f"App chooses to use target_image_size={self.target_image_size} bytes")

    def process_user_request(self):
        """Iterate over each input directory/PDFs and generate compressed PDF files"""
        for input_path in self.user_input:
            input_path = input_path.strip()
            if not os.path.exists(input_path):
                logger.error(f"ERROR: input path {input_path} does not exist.\n")
                continue

            if image_functions.is_image_file(input_path):
                self.reduce_single_image_file_size(input_path)
                logger.info(f"SUCCESS: File {input_path} processed.\n")

            elif file_functions.is_directory(input_path):
                self._process_directory(input_directory=input_path)
                logger.info(f"SUCCESS: Directory {input_path} processed.\n")

    def _process_directory(self, input_directory: str):
        """Notice, it's a recursive function.

        Process a single input directory by finding PDF files and then generating
        snapshots of each PDF and subsequently processing the sub-directories of the
        input directory as well.
        :param input_directory (str): The path to the input directory.
        """
        image_file_paths = image_functions.list_image_files(input_directory)
        for image_path in image_file_paths:
            self.reduce_single_image_file_size(image_path)

        sub_directories = file_functions.list_directories(input_directory)
        for directory in sub_directories:
            self._process_directory(directory)

    def calculate_compress_image_size_in_bytes(self, file_path: str) -> int:
        """
        This function calculates the desired size of the target compressed file in bytes

        :param file_path: absolute file path
        :return: int
        """
        compress_file_size_in_byte = self.target_image_size  # bytes

        if not self.target_image_size:  # notice target_image_size has high priority
            file_size_in_byte = file_functions.get_file_size_in_bytes(file_path)
            compress_file_size_in_byte = file_size_in_byte * (
                        1 - (self.reduction_quality_percentage / 100))

        return compress_file_size_in_byte

    def reduce_single_image_file_size(self, input_path):

        # Calculate the target file size based on the reduction percentage / target size
        target_img_size = self.calculate_compress_image_size_in_bytes(input_path)
        file_extension, _ = file_functions.get_file_extension(input_path)

        image = Image.open(input_path)

        # Save the image with optimized compression at different quality levels
        with tempfile.TemporaryDirectory() as temp_dir:
            for quality in range(98, 2, -2):

                temp_img_path = os.path.join(temp_dir, f'temp_{file_extension}')
                image.save(temp_img_path, optimize=True, quality=quality)

                temp_img_size = file_functions.get_file_size_in_bytes(temp_img_path)
                if temp_img_size <= target_img_size:
                    # todo: write a function to get unique name for img
                    output_path = self.get_output_path(input_path, quality)
                    image.save(output_path, optimize=True, quality=quality)
                    return output_path

        logger.warning(f"File {input_path}: not possible to reduce quality. "
                       f"Decrease reduction in quality")
        return None

    def get_output_path(self, input_path, quality):
        # todo: rewrite it as 'get_unique_path_for_compressed_pdf' is defined in file 'compressPDF/app/pdf_compressor.py'
        dest_dir = self.user_dest_path if self.user_dest_path else \
            file_functions.get_directory_name(input_path)

        file_name = file_functions.get_file_name(input_path)
        file_name = f'Q{quality}_{file_name}'
        file_path = os.path.join(dest_dir, file_name)
        file_path = file_functions.get_unique_filepath_in_same_dir(file_path)
        return file_path

# # Example usage
# # input_path = 'path/to/your/image.jpg'
# input_path = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\document bank\manisha docs\manisha last 4 months bank statements\chequing account\pdf-snapshots\New folder\chequing-april-2023-page-1.jpg'
# reduction_percentage = 20  # Reduce file size by 20%
#
# output_path = reduce_image_file_size(input_path, reduction_percentage)
# if output_path:
#     print(f"Compressed image saved at: {output_path}")
# else:
#     print("Failed to compress image within the specified reduction percentage.")


aa = ImageSizeReducer(user_input=[r'C:\Users\MANTKUMAR\Downloads\experiments\mk'],user_dest_path=r'C:\Users\MANTKUMAR\Downloads\experiments\output')
import pdb;pdb.set_trace()
aa.process_user_request()
