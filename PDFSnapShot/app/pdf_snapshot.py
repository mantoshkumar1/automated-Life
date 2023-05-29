import os
from pdf2image import convert_from_path
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
        ├── pdf_file_1.pdf
        ├── pdf_file_2.pdf
        ├── pdf-snapshots
        │   ├── pdf_file_1_page_1.jpg
        │   ├── pdf_file_2_page_1.jpg
        │   └── pdf_file_2_page_2.jpg
        ├── subdirectory
        │   ├── subdirectory_pdf.pdf
        │   └── pdf-snapshots
        │       └── subdirectory_pdf_page_1.jpg
        └── ...

    How To Use This Tool:
    ----------------------
        1. Initialize an instance of the PDFSnapshotGenerator class by passing a list
           of input directories as a parameter.
        2. Call the generate_snapshots method to start the generation process.
    """
    def __init__(self, input_directories: List[str]):
        """
        :param input_directories (list): A list of input directories where the PDF files are located.
        """
        self.input_directories = input_directories

    def generate_snapshots(self):
        """Iterate over each input directory and generate JPEG image of each page in PDF files"""
        for input_directory in self.input_directories:
            input_directory = input_directory.strip()
            if not os.path.exists(input_directory):
                logger.error(f"ERROR: input directory {input_directory} does not exist.\n")
                continue
            self._process_directory(input_directory)
            logger.info(f"SUCCESS: {input_directory} processed completed.\n")

    def _process_directory(self, input_directory: str):
        """Process a single input directory by finding PDF files and calling the required operations.
        :param input_directory (str): The path to the input directory.
        """
        pdf_file_paths = self._find_pdf_files(input_directory)
        self._generate_snapshots(pdf_file_paths)
        self._process_subdirectories(input_directory)

    def _find_pdf_files(self, directory: str) -> list:
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

    def _generate_snapshots(self, pdf_file_paths: List[str]):
        """Generate JPEG image of each page within the PDF files
        :param pdf_file_paths (list <str>): A list of paths to the PDF files to process.
        """
        for pdf_file_path in pdf_file_paths:
            image_objects = self._convert_pdf_to_images(pdf_file_path)
            self._save_images(image_objects, pdf_file_path)

    def _process_subdirectories(self, directory: str):
        """Process subdirectories within the given directory
        :param directory (str): The path to the directory to process.
        """
        for root, dirs, _ in os.walk(directory):
            for dir_name in dirs:
                self._process_directory(os.path.join(root, dir_name))

    def _convert_pdf_to_images(self, pdf_path: str) -> list:
        """Convert each page of the PDF to a list of PIL Image objects
        :param pdf_path (str): The path to the PDF file to convert.
        :returns A list of PIL Image objects representing each page of the PDF.
        """
        return convert_from_path(pdf_path)

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
        filename = os.path.basename(pdf_path)
        output_directory = os.path.join(os.path.dirname(pdf_path), 'pdf-snapshots')
        if not os.path.exists(output_directory):
            logger.info(f"SUCCESS: output directory {output_directory} created\n")
        os.makedirs(output_directory, exist_ok=True)  # Create pdf-snapshots directory if it doesn't exist
        for i, image in enumerate(image_objects):
            image_path = os.path.join(output_directory, f"{filename}_page_{i + 1}.jpg")
            image.save(image_path, "JPEG")

# # Usage example
# input_directories = ['/path/to/pdf/files/in/C/drive', '/path/to/pdf/files/in/D/drive']
# generator = PDFSnapshotGenerator(input_directories)
# generator.generate_snapshots()
#

