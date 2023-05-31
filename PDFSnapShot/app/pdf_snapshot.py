import os
import pdf2image
from typing import List

from utility.logger_util.setup_logger import logger


class PDFSnapshotGenerator:
    """
    The PDFSnapshotGenerator class provides a convenient way to iterate over a
    list of input directories, locate PDF files within each directory (including
    subdirectories), and generate JPEG snapshots of each page of the PDF files.

    Each generated image is stored in the same location as the source PDF file,
    within a directory named "pdf-snapshots".

    Once execution completes, this will be the final structure of each directory
    inside user-given input directories.
        input_directory
        ├── pdf_file_1.pdf  <== Has two pages
        ├── pdf_file_2.pdf  <== Has one page only
        ├── pdf-snapshots   <== Default Destination Directory of Generated images
        │   ├── pdf_file_1-page-1.jpg
        │   ├── pdf_file_2-page-1.jpg
        │   └── pdf_file_2-page-2.jpg
        ├── subdirectory
        │   ├── subdirectory_pdf.pdf  <== Has one page only
        │   └── pdf-snapshots         <== Default Destination Directory of Generated images
        │       └── subdirectory_pdf-page-1.jpg
        └── ...

    How To Use This Tool:
    ----------------------
        1. Initialize an instance of the PDFSnapshotGenerator class by passing a list
           of input directories as a parameter.
        2. Call the generate_snapshots method to start the generation process.
    """
    def __init__(self, user_input: List[str], user_dest_path: str = ''):
        """
        :param user_input (list): A list of input directories/PDFs where the PDF files are located.
        :param user_dest_path (str): User specified optional destination directory to store generated images
        """
        self.user_input = user_input
        self.user_dest_path: str = user_dest_path

    def generate_pdf_snapshots(self):
        """Iterate over each input directory/PDFs and generate JPEG image of each page in PDF files"""
        for input_path in self.user_input:
            input_path = input_path.strip()
            if not os.path.exists(input_path):
                logger.error(f"ERROR: input path {input_path} does not exist.\n")
                continue

            if PDFSnapshotGenerator.is_file(input_path):  # PDF file
                self._generate_pdf_snapshots(pdf_file_path=input_path)
            else:  # Directory
                self._process_directory(input_directory=input_path)
            logger.info(f"SUCCESS: {input_path} processed.\n")

    def _generate_pdf_snapshots(self, pdf_file_path: str):
        """Generate JPEG image of each page within the PDF files
        :param pdf_file_path (<str>): A path to a PDF file to process.
        """
        if not os.path.exists(pdf_file_path):
            logger.error(f"ERROR: PDF {pdf_file_path} does not exist")
            return
        image_objects = self._convert_pdf_to_images(pdf_path=pdf_file_path)
        self._save_images(image_objects=image_objects, pdf_path=pdf_file_path)

    def _process_pdfs_files(self, pdf_file_paths: List[str]):
        """Process each PDF file to generate JPEG image of each page within the PDF.
        :param pdf_file_paths (list <str>): A list of paths to the PDF files to process.
        """
        for pdf_file_path in pdf_file_paths:
            if not os.path.exists(pdf_file_path):
                logger.error(f"ERROR: PDF {pdf_file_path} does not exist")
                continue
            self._generate_pdf_snapshots(pdf_file_path=pdf_file_path)

    def _process_directory(self, input_directory: str):
        """Process a single input directory by finding PDF files and then generating
        snapshots of each PDF and subsequently processing the sub-directories of the
        input directory as well.
        :param input_directory (str): The path to the input directory.
        """
        pdf_file_paths = self._find_pdf_files(directory=input_directory)
        self._process_pdfs_files(pdf_file_paths=pdf_file_paths)
        self._process_subdirectories(directory=input_directory)

    @classmethod
    def _find_pdf_files(cls, directory: str) -> list:
        """Finds all PDF files within a given directory, including subdirectories.
        :param directory (str): The path to the directory to search for PDF files.
        :returns A list of paths to the PDF files found in a directory.
        """
        pdf_file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.pdf'):
                    pdf_file_paths.append(os.path.join(root, file))
        return pdf_file_paths

    def _process_subdirectories(self, directory: str):
        """Process subdirectories within the given directory
        :param directory (str): The path to the directory to process.
        """
        for root, dirs, _ in os.walk(directory):
            for dir_name in dirs:
                self._process_directory(os.path.join(root, dir_name))

    @classmethod
    def _convert_pdf_to_images(cls, pdf_path: str) -> list:
        """Convert each page of the PDF to a list of PIL Image objects
        :param pdf_path (str): The path to the PDF file to convert.
        :returns A list of PIL Image objects representing each page of the PDF.
        """
        return pdf2image.convert_from_path(pdf_path)

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

    def _save_images(self, image_objects: list, pdf_path: str):
        """Save each image with the file name and page number.

        How naming of each PDF page is decided:
        ----------------------------------------------
        The names of the images are decided based on a pattern of {PDF_filename}_{page_number}.jpg.
        The PDF_filename represents the base name of the PDF file without the file extension, and
        the page_number indicates the page number of the image. By combining these two elements,
        each image is given a unique name that includes both the original PDF filename and the
        corresponding page number. This naming scheme helps in identifying and organizing the
        images according to their respective pages within the PDF file.

        :param image_objects (list): A list of PIL Image objects representing the converted images of each pages of the PDF.
        :param pdf_path (str): The path to the original PDF file. Used for naming the output images.
        """
        src_filename = os.path.basename(pdf_path)
        output_directory = self.user_dest_path if self.user_dest_path else \
            os.path.join(os.path.dirname(pdf_path), 'pdf-snapshots')

        # Create pdf-snapshots directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)
            logger.info(f"SUCCESS: output directory {output_directory} created\n")

        for i, image in enumerate(image_objects):
            # strip extension (.pdf) from filename
            src_filename_without_extension, _ = os.path.splitext(src_filename)
            dest_image_path = os.path.join(output_directory, f"{src_filename_without_extension}-page-{i + 1}.jpg")
            image.save(dest_image_path, "JPEG")


# # Usage example
# input_paths = ['/path/to/pdf/file/in/C/drive', '/path/to/directory/conataining/PDF/files/in/D/drive']
# generator = PDFSnapshotGenerator(input_paths)
# generator.generate_snapshots()
#

