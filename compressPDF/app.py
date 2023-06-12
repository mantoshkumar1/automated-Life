import fitz
from pdf2image import convert_from_path
import tempfile
import os

def func_reduce_pdf_size(input_path, output_path):
    pdf_document = fitz.open(input_path)
    pdf_document.save(output_path, deflate=True)
    pdf_document.close()

    print("PDF size reduced successfully!")

def reduce_pdf_size(input_path, output_path, quality=85):
    images = convert_from_path(input_path, dpi=150)  # Convert PDF pages to images: 96/150

    writer = fitz.open()

    with tempfile.TemporaryDirectory() as temp_dir:
        for i, image in enumerate(images):
            img_path = os.path.join(temp_dir, f'temp_{i}.jpg')

            image.save(img_path, 'JPEG', quality=quality)

            page = writer.new_page(width=image.width, height=image.height)
            page.insert_image(fitz.Rect(0, 0, image.width, image.height), filename=img_path)

        # if os.path.isfile(output_path):
        file_name, file_ext = os.path.splitext(output_path)
        output_path = file_name + f'_{quality}q{file_ext}'

        writer.save(output_path)

    print("PDF size reduced successfully!")

# Usage example
input_file = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\2023 canada visitor visa application\working-on-package\MIL\invitation letter\v2.0-PunamKumari-invitation-letter.pdf'  # Specify the path to your input PDF file
output_file = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\2023 canada visitor visa application\working-on-package\MIL\invitation letter\flattern.pdf'  # Specify the path to the output PDF file

input_file = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\2023 canada visitor visa application\working-on-package\FIL\invitation letter\v2.0-KrishnaPrasad-invitation-letter.pdf'
output_file = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\2023 canada visitor visa application\working-on-package\FIL\invitation letter\flattern.pdf'  # Specify the path to the output PDF file
func_reduce_pdf_size(input_file, output_file)

# input_file = output_file
output_file = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\2023 canada visitor visa application\working-on-package\MIL\invitation letter\output.pdf'  # Specify the path to the output PDF file
output_file = r'C:\Users\MANTKUMAR\Documents\mantosh-backup-gdrive\101-family-safe-backup\inLaw-personal-documents\2023 canada visitor visa application\working-on-package\FIL\invitation letter\output.pdf'
reduce_pdf_size(input_file, output_file, quality=75)

