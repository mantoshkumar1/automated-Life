import os
from typing import List
import fitz  # PyMuPDF
from compressPDF.app.pdf_compressor import PDFCompressor

class PDFSorterMerger:
    def __init__(self, user_input: List[str], user_dest_path: str = '', target_pdf_size=None):
        """
        :param user_input (list): A list of input directories/PDFs where the PDF files are located.
        :param user_dest_path (str): User specified optional destination directory to store generated images
        :param target_pdf_size: (float) Target PDF size of each PDF in MB.
        """
        self.user_input_pdf_dir_list = user_input # list of directory paths
        self.user_dest_path: str = user_dest_path
        self.target_pdf_size = target_pdf_size

    def process_user_request(self):
        for pdf_dir in self.user_input_pdf_dir_list:
            self.merge_pdfs(pdf_dir)

    def sort_files(self, files):
        # Sort files numerically and then alphabetically
        files.sort(key=lambda f: (int(''.join(filter(str.isdigit, f)) or 0), f))
        return files

    def merge_pdfs(self, pdf_dir: str):
        # Get list of PDF files in the directory
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

        # Sort the PDF files
        sorted_files = self.sort_files(pdf_files)

        # Create a new PDF document (for merged one)
        merged_pdf = fitz.open()

        # Iterate over sorted PDF files and append their pages to the merged PDF
        for pdf_file in sorted_files:
            pdf_document = fitz.open(os.path.join(pdf_dir, pdf_file))
            for page_num in range(pdf_document.page_count):
                merged_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        # Save the merged PDF
        merge_pdf_dest_dir = self.user_dest_path if self.user_dest_path else pdf_dir
        merged_pdf_path = os.path.join(merge_pdf_dest_dir, "merged_output.pdf")
        merged_pdf.save(merged_pdf_path)
        if self.target_pdf_size > 0:
            merge_compressed_pdf = PDFCompressor(user_input=[merged_pdf_path], user_dest_dir=merge_pdf_dest_dir, target_pdf_size=self.target_pdf_size)
            merge_compressed_pdf.process_user_request()
            os.remove(merged_pdf_path)



# Example usage
# directory = ["path_to_pdf_directory"]  # Replace with the actual directory path
# pdf_sorter_merger = PDFSorterMerger(directory)
# pdf_sorter_merger.process_user_request()