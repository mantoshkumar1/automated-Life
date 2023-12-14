import fitz
from pdf2image import convert_from_path
import os
import tempfile
from typing import List
import shutil

from utility.logger_util.setup_logger import logger
from utility import file_functions
from utility import pdf_functions


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

            if pdf_functions.is_pdf(file_path=input_path):
                self.reduce_pdf_size(input_pdf_path=input_path)
                logger.info(f"SUCCESS: File {input_path} processed.\n")

            elif file_functions.is_directory(path=input_path):  # Directory
                self._process_directory(input_directory=input_path)
                logger.info(f"SUCCESS: Directory {input_path} processed.\n")

    def copy_pdf_file(self, source_pdf_path: str):
        """If user has specified a path to store the compressed PDF, copy the file
        there. Otherwise, create a directory 'compressed-pdf' in source directory of
        PDF file and store a copy of PDF there.

        :param source_pdf_path: absolute path
        :return:
        """
        compressed_pdf_file_path, compressed_pdf_dir_path = \
            self.get_unique_path_for_compressed_pdf(source_pdf_path)

        file_functions.create_directory(compressed_pdf_dir_path)

        shutil.copy(source_pdf_path, compressed_pdf_file_path)

        print(f"Compressed file is stored in directory: {compressed_pdf_dir_path}")
        print('.' * 45)

    def get_unique_path_for_compressed_pdf(self, file_path: str) -> (str, str):
        """
        This function finds an unique non-existing path for the newly created
        compressed PDF file.

        :param file_path: absolute file path
        :return: (absolute path for new compressed PDF, absolute of PDF directory)
        """
        pdf_dest_dir = self.user_dest_dir
        if not pdf_dest_dir:
            pdf_dest_dir = os.path.join(file_functions.get_directory_name(file_path), 'compressed-pdf')

        pdf_file_name = f'compressed_{file_functions.get_file_name(file_path)}'
        pdf_file_path = os.path.join(pdf_dest_dir, pdf_file_name)
        pdf_file_path = file_functions.get_unique_filepath_in_same_dir(pdf_file_path)

        return pdf_file_path, pdf_dest_dir

    def reduce_pdf_size(self, input_pdf_path: str):
        """Generate JPEG image of each page within the PDF files
        :param input_pdf_path: <str> A path to a PDF file to process.
        """
        print(f'Processing file "{os.path.basename(input_pdf_path)}"')

        if not os.path.exists(input_pdf_path):
            logger.error(f"ERROR: PDF {input_pdf_path} does not exist")
            return

        pdf_file_size = file_functions.get_file_size_in_mb(input_pdf_path)
        if pdf_file_size <= self.target_pdf_size:
            logger.debug(f"user must be kidding. Just copy his PDF.")
            self.copy_pdf_file(input_pdf_path)
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

                temp_pdf_file_size = file_functions.get_file_size_in_mb(temp_pdf_path)

                if temp_pdf_file_size < self.target_pdf_size:
                    # print(f"{os.path.basename(input_pdf_path)}: Reduced to {quality}%")

                    # Decide where you want to save the newly generated compressed PDF
                    compressed_pdf_file_path, compressed_pdf_dir_path = \
                        self.get_unique_path_for_compressed_pdf(input_pdf_path)

                    # create the destination directory for the compressed PDF
                    file_functions.create_directory(compressed_pdf_dir_path)

                    # save the PDF
                    writer.save(compressed_pdf_file_path)
                    print(f"File is stored in directory: {compressed_pdf_dir_path}")
                    print('.' * 45)
                    break

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
        pdf_file_paths = file_functions.list_files(
            directory=input_directory, file_extensions=['.pdf'])

        list_dir = file_functions.list_directories(input_directory)
        self._process_pdfs_files(pdf_file_paths=pdf_file_paths)

        for directory in list_dir:
            self._process_directory(directory)
