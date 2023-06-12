from PIL import Image
import os
import pathlib
from typing import List

from utility.logger_util.setup_logger import logger

"""
https://www.cic.gc.ca/english/helpcentre/answer.asp?qnum=1213
- Saving your images at a lower resolution, such as 96 DPI or 150 DPI, can greatly reduce image file size.

"""


class ImageSizeReducer:
    def __init__(self, user_input: List[str], user_dest_path: str = ''):
        self.user_input = user_input
        self.user_dest_path: str = user_dest_path

    def reduce_image_sizes(self):
        """Iterate over each input directory/images and reduce the image file sizes of each image"""
        for input_path in self.user_input:
            input_path = input_path.strip()
            if not os.path.exists(input_path):
                logger.error(f"ERROR: input path {input_path} does not exist.\n")
                continue

            if ImageSizeReducer.is_file(input_path):  # file
                self._generate_pdf_snapshots(pdf_file_path=input_path)
            else:  # Directory
                self._process_directory(input_directory=input_path)
            logger.info(f"SUCCESS: {input_path} processed.\n")

    @staticmethod
    def is_file(path) -> bool:
        """
        Returns True if given input path represents a file; returns False for
        directories. Raises FileNotFoundError for Non-existent file/folder path.
        :param path: str
        :return: bool
        """
        if not os.path.exists(path):
            raise FileNotFoundError
        if os.path.isfile(path):
            return True
        # must be directory
        return False

    def reduce_image_resolution(self, image_path, dpi):
        """This function takes the path of the original image and the desired DPI as parameters. It calculates the target width and height based on the desired DPI and the current DPI of the original image. Then, it resizes the image using the resize method with Lanczos resampling for better quality. Finally, it sets the DPI metadata for the resized image and saves it with the new DPI."""
        # Open the image using Pillow
        image = Image.open(image_path)

        # Calculate the target size based on the desired DPI
        target_width = int(image.width * dpi / image.info['dpi'][0])
        target_height = int(image.height * dpi / image.info['dpi'][1])
        target_size = (target_width, target_height)

        # Resize the image to the target size using Lanczos resampling for quality
        resized_image = image.resize(target_size, resample=Image.LANCZOS)

        # Set the DPI metadata for the resized image
        resized_image.info['dpi'] = (dpi, dpi)

        # Save the resized image with the new DPI
        resized_image.save("resized_image.jpg", dpi=(dpi, dpi))

# # Example usage
# image_path = "original_image.jpg"
# dpi = 96  # or 150
# reduce_resolution(image_path, dpi)
#
#############################################################################################

def reduce_image_file_size(input_path, reduction_percentage):
    image = Image.open(input_path)

    # Calculate the target file size based on the reduction percentage
    target_file_size = os.path.getsize(input_path) * (1 - (reduction_percentage / 100))

    # Save the image with optimized compression at different quality levels
    for quality in range(90, 10, -10):
        output_path = get_output_path(input_path, quality)
        image.save(output_path, optimize=True, quality=quality)

        # Check the file size of the saved image
        file_size = os.path.getsize(output_path)
        if file_size <= target_file_size:
            return output_path
        os.remove(output_path)

    return None

def get_output_path(input_path, quality):
    input_dir = pathlib.Path(input_path).parent
    input_name = pathlib.Path(input_path).stem
    output_name = f"output_{input_name}_q{quality}.jpg"
    return str(input_dir / output_name)

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
