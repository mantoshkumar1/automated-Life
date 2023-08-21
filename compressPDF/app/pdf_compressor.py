import fitz
from pdf2image import convert_from_path
import os
import tempfile
from typing import List
import shutil

from utility.logger_util.setup_logger import logger


class PDFCompressor:
    """
    The PDFCompressor class provides a convenient way to iterate over a
    list of input directories, locate PDF files within each directory (including
    subdirectories), and generate compressed PDF files of reduced size. Obviously,
    quality will be affected in the process.

    Each generated compressed PDF is stored in the same location as the source PDF file,
    within a directory named "compressed-pdf".

    Once execution completes, this will be the final structure of each directory
    inside user-given input directories.
        input_directory
        ├── pdf_file_1.pdf
        ├── pdf_file_2.pdf
        ├── compressed-pdf  <== Default Destination Directory of Generated compressed PDFs
        │   ├── reduced-quality-20-pdf_file_1.pdf
        │   ├── reduced-quality-80-pdf_file_2.pdf
        ├── subdirectory
        │   ├── subdirectory_pdf.pdf  <== Has one page only
        │   └── compressed-pdf  <== Default Destination Directory of Generated images
        │       └── reduced-quality-60-subdirectory_pdf.pdf
        └── ...

    How To Use This Tool:
    ----------------------
        1. Initialize an instance of the PDFCompressor class by passing a list
           of input directories as a parameter.
        2. Call the process_user_request method to complete the process.
    """
    def __init__(self, user_input: List[str], user_dest_dir: str = '', target_pdf_size=999):
        """
        :param user_input (list): A list of input directories/PDFs where the PDF files are located.
        :param user_dest_dir (str): User specified optional destination directory to store generated compressed PDFs.
        :param target_pdf_size: (float) Target PDF size of each PDF in MB.
        """
        self.user_input = user_input
        self.user_dest_dir: str = user_dest_dir
        self.target_pdf_size = target_pdf_size

    def process_user_request(self):
        """Iterate over each input directory/PDFs and generate compressed PDF files"""
        for input_path in self.user_input:
            input_path = input_path.strip()
            if not os.path.exists(input_path):
                logger.error(f"ERROR: input path {input_path} does not exist.\n")
                continue

            # if not PDF neither a directory
            if not PDFCompressor.is_pdf_or_directory(file_path=input_path):
                continue

            if PDFCompressor.is_file(input_path, file_extension='.pdf'):
                self.reduce_pdf_size(input_pdf_path=input_path)
            else:  # Directory
                self._process_directory(input_directory=input_path)
            logger.info(f"SUCCESS: {input_path} processed.\n")

    def copy_file(self, source_file_path):
        directory_path, file_name_with_extension = os.path.split(source_file_path)
        if self.user_dest_dir:
            directory_path = self.user_dest_dir
        output_path = os.path.join(directory_path, file_name_with_extension)
        if source_file_path != output_path:
            shutil.copy(source_file_path, output_path)
        print(f"Compressed file is stored in directory: {directory_path}")
        print('.' * 45)

    def reduce_pdf_size(self, input_pdf_path: str):
        """Generate JPEG image of each page within the PDF files
        :param input_pdf_path: <str> A path to a PDF file to process.
        """
        print(f'Processing file "{os.path.basename(input_pdf_path)}"')

        if not os.path.exists(input_pdf_path):
            logger.error(f"ERROR: PDF {input_pdf_path} does not exist")
            return

        pdf_file_size = PDFCompressor.get_file_size_in_mb(input_pdf_path)
        if pdf_file_size < self.target_pdf_size:
            self.copy_file(input_pdf_path)
            return

        images = convert_from_path(input_pdf_path, dpi=150)  # Convert PDF pages to images: 96/150

        quality = 100
        while quality > 2:
            quality -= 2
            # print(f"Processing to maintain {quality}% quality. File: {os.path.basename(input_pdf_path)}")

            # Important: Create a new PDF writer for each attempt to avoid appending to
            # an existing PDF.
            writer = fitz.open()

            with tempfile.TemporaryDirectory() as temp_dir:
                for i, image in enumerate(images):
                    img_path = os.path.join(temp_dir, f'temp_{i}.jpg')

                    image.save(img_path, 'JPEG', quality=quality)

                    page = writer.new_page(width=image.width, height=image.height)
                    page.insert_image(fitz.Rect(0, 0, image.width, image.height),
                                      filename=img_path)

                temp_pdf_path = os.path.join(temp_dir, f'temp_{quality}.pdf')
                writer.save(temp_pdf_path)
                temp_pdf_file_size = self.get_file_size_in_mb(temp_pdf_path)

                if temp_pdf_file_size < self.target_pdf_size:
                    # print(f"{os.path.basename(input_pdf_path)}: Reduced to {quality}%")
                    directory_path, file_name_with_extension = os.path.split(input_pdf_path)
                    if self.user_dest_dir:
                        directory_path = self.user_dest_dir
                    output_path = os.path.join(directory_path,
                                               f'reduced-quality-{quality}-{file_name_with_extension}')

                    index = 1
                    while os.path.isfile(output_path):
                        index += 1
                        output_path = os.path.join(directory_path,
                                                   f'dup{index}-reduced-quality-{quality}-{file_name_with_extension}')

                    writer.save(output_path)
                    print(f"File is stored in directory: {directory_path}")
                    print('.' * 45)
                    break

    @staticmethod
    def get_file_size_in_mb(file_path):
        """Returns file size in MB"""
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        return file_size_mb

    def _process_pdfs_files(self, pdf_file_paths: List[str]):
        """Process each PDF file to generate compressed PDF within specified target size in MB.
        :param pdf_file_paths (list <str>): A list of paths to the PDF files to process.
        """
        for pdf_file_path in pdf_file_paths:
            if not os.path.exists(pdf_file_path):
                logger.error(f"ERROR: PDF {pdf_file_path} does not exist")
                continue
            self.reduce_pdf_size(input_pdf_path=pdf_file_path)

    def _process_directory(self, input_directory: str):
        """Process a single input directory by finding PDF files and then generating
        snapshots of each PDF and subsequently processing the sub-directories of the
        input directory as well.
        :param input_directory (str): The path to the input directory.
        """
        pdf_file_paths = self._find_pdf_files(directory=input_directory)
        self._process_pdfs_files(pdf_file_paths=pdf_file_paths)

    @classmethod
    def _find_pdf_files(cls, directory: str) -> list:
        """Finds all PDF files within a given directory, including subdirectories.
        :param directory (str): The path to the directory to search for PDF files.
        :returns A list of paths to the PDF files found in a directory.
        """
        pdf_file_paths = []
        for root, _, files in os.walk(directory): # traverses recursively top-down
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file_paths.append(os.path.join(root, file))
        return pdf_file_paths

    @staticmethod
    def is_file(path, file_extension='.pdf') -> bool:
        """
        Returns True if given input path represents a PDF; returns False for
        directories. Raises FileNotFoundError for Non-existent file/folder path.
        :param path: str
        :param file_extension: str
        :return: bool
        """
        if not os.path.exists(path):
            raise FileNotFoundError
        if os.path.isfile(path):
            if not file_extension:
                return True
            if path.lower().endswith(file_extension):
                return True

        # must be directory or file with non-expected extension
        return False

    @staticmethod
    def is_pdf_or_directory(file_path):
        """The function returns True because it's either a PDF file or a regular file.
        Otherwise, it returns False."""
        return os.path.isdir(file_path) or (
                    os.path.isfile(file_path) and file_path.lower().endswith('.pdf'))
