import os
from PIL import Image
from typing import List

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from utility import file_functions
from utility.logger_util.setup_logger import logger


class Image2PDF:
    """Merge multiple JPEG images into a single PDF document."""

    def __init__(self, user_input_dir: str, user_dest_dir: str = ''):
        """
        :param user_input_dir: The input directory where the image files are located.
        :param user_dest_dir (str): User specified optional destination directory to
            store the generated PDF file.
        """
        self.user_input_dir = user_input_dir
        self.user_dest_dir: str = user_dest_dir

        # todo: 10 June 2024: As of now, it's only taking JPG files, modifiy it to
        #  handle any image file. At this moment, I don't need it so not adding it.

        # todo: 10 June 2024: As of now, it only supports only one directory and does
        #  not look into sub-directories. I don't need it at this time, this is the
        #  reason I am not adding this feature. Perhaps, in future, make it capable
        #  to handle more than one directories, nested directories.

    def convert_jpg_to_pdf(self, input_folder: str, output_pdf_abs_path: str) -> None:
        """
           Convert multiple JPEG images into a single PDF document.

           Parameters:
           - input_folder (str): Path to the folder containing JPEG images.
           - output_pdf_abs_path (str): Absolute path of the output PDF file.

           Returns:
           - None

           Description:
           This function converts multiple JPEG images located in the specified input folder
           into a single PDF document. It iterates through the JPEG files, resizes each image
           to fit the page width of the PDF document while maintaining the aspect ratio, and
           adds them to the PDF document sequentially. The resulting PDF document contains
           all the input images merged into a cohesive file.
        """

        # Get a list of jpg files sorted alphabetically
        # todo (10 June 2024): As of now, only support jpg, make it support all image formats.
        jpg_files = [file for file in os.listdir(input_folder) if file.endswith('.jpg')]
        sorted_jpg_files = file_functions.sort_filenames_numerically(jpg_files)

        # Create a PDF
        c = canvas.Canvas(output_pdf_abs_path, pagesize=letter)
        width, height = letter

        for jpg_file in sorted_jpg_files:
            # Open JPEG image
            img = Image.open(os.path.join(input_folder, jpg_file))

            # Calculate aspect ratio
            aspect_ratio = img.width / img.height

            # Resize image to fit the page width
            img_width = width
            img_height = width / aspect_ratio

            # Add image to PDF
            c.drawImage(os.path.join(input_folder, jpg_file), 0, 0, width=img_width, height=img_height)
            c.showPage()

        c.save()
        logger.info(f'Image2PDF: Merged PDF is stored at absolute path: "{output_pdf_abs_path}"')

    def get_unique_path_for_resulting_pdf(self) -> (str, str):
        """
        This function finds an unique non-existing path for PDF file that we want
        to create.

        :return: (absolute path for new PDF, absolute of PDF directory)
        """
        pdf_dest_dir = self.user_dest_dir

        if not pdf_dest_dir:
            pdf_dest_dir = self.user_input_dir

        pdf_file_name = f'merged_images_into_pdf.pdf'
        pdf_file_path = os.path.join(pdf_dest_dir, pdf_file_name)
        pdf_file_path = file_functions.get_unique_filepath_in_same_dir(pdf_file_path)
        return pdf_file_path, pdf_dest_dir

    def process_user_request(self):
        """Merge all image files in a PDF. The images files will be sorted alphabetically"""
        # check if user_input_dir exists
        user_input_folder = self.user_input_dir.strip()
        if not os.path.exists(user_input_folder):
            logger.error(f"ERROR: input folder {user_input_folder} does not exist.\n")
            return

        # absolute path of the resulting PDF containing all images
        output_pdf_file_path, _ = self.get_unique_path_for_resulting_pdf()

        if file_functions.is_directory(path=user_input_folder):  # Directory
            self.convert_jpg_to_pdf(input_folder=user_input_folder, output_pdf_abs_path=output_pdf_file_path)
            logger.info(f"SUCCESS: Directory {user_input_folder} processed.\n")


# Usage example:
# input_folder = r'C:\Users\Username\Downloads\test'
# img_to_pdf = Image2PDF(user_input_dir=input_folder, user_dest_dir='')
# img_to_pdf.process_user_request()
