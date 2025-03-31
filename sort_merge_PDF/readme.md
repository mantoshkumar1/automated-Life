# Sort_Merge_PDF

## What it Does:
This project sorts PDF files in a specified directory first numerically and then alphabetically by their filenames. 
It then merges the pages of these sorted PDFs into a single PDF file.

## 2. How to Run this Application?
* `cd automated-Life` <br /> 
* `python sort_merge_PDF\run.py --input-paths "C:\Users\MANTKUMAR\Downloads\delete" --dest-dir="C:\Us
ers\MANTKUMAR\Downloads\del" --target-pdf-size 2`

**usage: run.py [-h] --input-paths INPUT_DIRS [--dest-dir DEST_DIR] --target-pdf-size TARGET_PDF_SIZE (in MB)**

* `input-paths` is a mandatory string field. Provide the directory path that contains your PDF files. You can also specify PDF file paths. Just make sure that they are separated by comma. The whole input should be a string.
* `dest-dir` is an optional string field. If you do not use this argument then the merged PDF file gets stored in the same directory where the original PDF is stored. The name of the reduced sized PDF will be `compressed_merged_output.pdf`.
* `target-pdf-size` is an optional integer field. This argument specifies your desired size of the merged PDF in MB. Default is `0`, which means, no compression needed.


## How to Setup Dependencies:
1. Add the root directory of this repo to `PYTHONPATH` User variable.
2. Install Required Dependencies: Ensure you have Python 3.x installed. Then, install the required library: `pip install -r sort_merge_PDF/requirements.txt`
3. Install Poppler: Follow these steps to install Poppler on Windows:
   1. Download Poppler for Windows:
      * Visit the Poppler for Windows page.
      * Download the latest release (e.g., poppler-21.12.0_x86.7z).
   2. Extract the Archive:
      * Extract the downloaded .7z file to a directory, for example, C:\Program Files\poppler-21.12.0_x86.
   3. Add Poppler to System PATH:
      * Open the Start menu and search for "Edit the system environment variables".
      * Click on "Environment Variables...".
      * Under "System variables", find and select the PATH variable, then click "Edit...".
      * Click "New" and add the path to the bin directory of Poppler, e.g., C:\Program Files\poppler-21.12.0_x86\Library\bin.
      * Click "OK" to close all dialogs.
      * Reboot system
4. Verify Installation:
      * Open a new Command Prompt and type pdfinfo. If Poppler is correctly installed and in the PATH, you should see usage information for pdfinfo.
5. Run the Script: Replace "path_to_pdf_directory" in the script with the actual path to your PDF files directory and run the script:
   `python .\sort_merge_PDF\run.py --input-paths "C:\Users\mantkumar\Downloads\bill"  --target-pdf-size 2`

## Motivation:
The motivation behind this project is to simplify the process of organizing and merging multiple PDF files, making it 
easier to manage and access combined documents.

On 31 Mar 2025, I had to submit my internet expenses to my employer. I had a 6-page bill spread across 3 PDFs. 
This task repeats every quarter. Who wants to do it manually again and again?

## How it Works:
1. The script lists all PDF files in the specified directory.
2. It sorts the files numerically and then alphabetically by their filenames.
3. It merges the pages of the sorted PDFs into a single PDF file at specified
    destination directory and if destination directory is not provided then it writes the merged PDF in the source directory itself.

## Benefits:
- *Convenience*:  Easily organize and merge multiple PDF files.
- *Efficiency*: Quickly sort and combine PDFs with minimal effort.
- *Customization*: Adapt the script to fit specific sorting and merging needs.
- *Productivity*: Save time and streamline document management.

## Future TODO:
* 31 Mar 2025: Add functionality to handle subdirectories and more complex sorting criteria.

## Requirements:
- Python 3.x
- PyMuPDF
- pdf2image
- Poppler

## Contributors:
- Mantosh Kumar

## License:
This project is licensed under the [MIT License](LICENSE).
