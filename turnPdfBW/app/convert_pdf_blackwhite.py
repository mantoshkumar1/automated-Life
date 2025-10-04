import os
from pdf2image import convert_from_path
from typing import List
from utility.logger_util.setup_logger import logger
from utility import pdf_functions
from utility import file_functions
from pdf2image.exceptions import PDFPageCountError


class PDFBlackWhiteConverter:
    """
    A class to convert any PDF file into a black-and-white (1-bit) PDF.
    """

    def __init__(self, user_input: List[str], pdf_quality: int, user_dest_path: str = ''):
        """
        :param user_input (list): A list of input directories/PDFs where the PDF files are located.
        :param user_dest_path (str): User specified optional destination directory to store generated images
        :param pdf_quality: (int) Quality percentage of generated B&W PDFs
        """
        self.user_input = user_input
        self.user_dest_path: str = user_dest_path
        self.pdf_quality = int(pdf_quality)

    def convert_all_pdfs_to_BW(self):
        """Iterate over each input directory/PDFs and generate equivalent Black and White PDF files"""
        for input_path in self.user_input:
            input_path = input_path.strip()
            if not os.path.exists(input_path):
                logger.error(f"ERROR: input path {input_path} does not exist.\n")
                continue

            # if not PDF neither a directory
            if not pdf_functions.is_pdf_or_directory(file_path=input_path):
                continue

            if file_functions.is_file(input_path, file_extension='.pdf'):
                self.convert_pdf_to_bw(pdf_file_path=input_path)
            else:  # Directory
                self._process_directory(input_directory=input_path)
            logger.info(f"SUCCESS: {input_path} processed.\n")

    def get_unique_path_for_BW_pdf(self, file_path: str) -> (str, str):
        """
        This function finds an unique non-existing path for the newly created BW PDF file.

        :param file_path: absolute file path
        :return: (absolute path for new compressed PDF, absolute of PDF directory)
        """
        pdf_dest_dir = self.user_dest_path
        if not pdf_dest_dir:
            pdf_dest_dir = os.path.join(file_functions.get_directory_name(file_path), 'BW-pdf')

        pdf_file_name = f'BW_{file_functions.get_file_name(file_path)}'
        pdf_file_path = os.path.join(pdf_dest_dir, pdf_file_name)
        pdf_file_path = file_functions.get_unique_filepath_in_same_dir(pdf_file_path)

        return pdf_file_path, pdf_dest_dir

    def quality_to_dpi(self):
        if self.pdf_quality <= 30:
            return 300 # Low quality, small file, good for text-only PDFs
        elif self.pdf_quality <= 60:
            return 600 # Medium quality, balanced for images and text
        else:
            return 900 # High quality, preserves detailed images, large file

    def convert_pdf_to_bw(self, pdf_file_path):
        print(f'Processing file "{os.path.basename(pdf_file_path)}"')

        if not os.path.exists(pdf_file_path):
            logger.error(f"ERROR: PDF {pdf_file_path} does not exist")
            return ''

        # Convert PDF pages to images
        try:
            pdf_quality = self.quality_to_dpi()
            pdf_pages = convert_from_path(pdf_file_path, dpi=pdf_quality)
        except PDFPageCountError:
            logger.error(f"Skipping encrypted or unreadable PDF: {pdf_file_path}")
            return ''

        bw_pages = []

        for page in pdf_pages:
            # Convert each page to black and white (1-bit pixels)
            bw_page = page.convert("1")
            bw_pages.append(bw_page)

        # Decide where you want to save the newly generated BW PDF
        bw_pdf_file_path, bw_pdf_dir_path = self.get_unique_path_for_BW_pdf(pdf_file_path)

        # create the destination directory for the BW PDF
        file_functions.create_directory(bw_pdf_dir_path)

        # Save all pages as a single PDF
        bw_pages[0].save(bw_pdf_file_path, save_all=True, append_images=bw_pages[1:])

        print(f"Black & white PDF saved in directory: {bw_pdf_dir_path}")
        return bw_pdf_file_path

    def _process_pdfs_files(self, pdf_file_paths: List[str]):
        """Process each PDF file to generate compressed PDF within specified target size in MB.
        :param pdf_file_paths (list <str>): A list of paths to the PDF files to process.
        """
        for pdf_file_path in pdf_file_paths:
            if not os.path.exists(pdf_file_path):
                logger.error(f"ERROR: PDF {pdf_file_path} does not exist")
                continue
            self.convert_pdf_to_bw(pdf_file_path=pdf_file_path)

    def _process_directory(self, input_directory: str):
        """Process a single input directory by finding PDF files and then generating
        snapshots of each PDF and subsequently processing the sub-directories of the
        input directory as well.
        :param input_directory (str): The path to the input directory.
        """
        pdf_file_paths = file_functions.list_files(
            directory=input_directory, file_extensions=['.pdf'])

        list_dir = file_functions.list_directories(input_directory)
        self._process_pdfs_files(pdf_file_paths=pdf_file_paths)

        for directory in list_dir:
            self._process_directory(directory)

# Example usage
if __name__ == "__main__":
    input_pdf_file = "example.pdf"
    converter = PDFBlackWhiteConverter([input_pdf_file])
    converter.convert_all_pdfs_to_BW()
