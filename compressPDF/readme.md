## 1. What Does This Application Do?

First of all, what was the need for this application?

During my stay in Canada, I had to file a lot of visa-related applications, and those 
applications had a limitation on the size of the PDF. Obviously, there are online tools 
available, but I didn't like them for two reasons:
1. I didn't want to share my sensitive documents with any third party. I don't trust them.
2. Those online tools didn't offer a lot of flexibility. Either, they would reduce the PDF size to such an extent that the whole document becomes blurry.

So, I decided to create my own app that does what I need.

**This application allows you to specify what your target size of the PDF is and does 
its magic to create a duplicate PDF within your target PDF size.**

## 2. How to Run this Application?
* `cd automated-Life` <br /> 
* `python compressPDF\run.py --input-paths "C:\Users\MANTKUMAR\Downloads\delete" --dest-dir="C:\Us
ers\MANTKUMAR\Downloads\del" --target-pdf-size 2`

**usage: run.py [-h] --input-paths INPUT_DIRS [--dest-dir DEST_DIR] --target-pdf-size TARGET_PDF_SIZE (in MB)**

* `input-paths` is a mandatory string field. Provide the directory path that contains your PDF files. You can also specify PDF file paths. Just make sure that they are separated by comma. The whole input should be a string.
* `dest-dir` is an optional string field. If you do not use this argument then the reduced sized PDF file gets stored in the same directory where the original PDF is stored. The name of the reduced sized PDF will start with `compressed-originalFileName.pdf`
* `target-pdf-size` is a mandatory integer field. This argument specifies your desired size of PDF in MB.

### 3. How to Setup Dependencies:
1. Install Python 3.6 or higher
2. Add the root directory of this repo to `PYTHONPATH` User variable.
3. Install Required Dependencies: Ensure you have Python 3.x installed. Then, install the required library: `pip install -r  compressPDF/requirements.txt`
4. Install Poppler: Follow these steps to install Poppler on Windows:
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
5. Verify Installation:
      * Open a new Command Prompt and type pdfinfo. If Poppler is correctly installed and in the PATH, you should see usage information for pdfinfo.
6. Run the Script: Replace "path_to_pdf_directory" in the script with the actual path to your PDF files directory and run the script:
   `cd automated-Life` <br />
   `python compressPDF\run.py --input-paths "C:\Users\MANTKUMAR\Downloads\delete" --dest-dir="C:\Users\MANTKUMAR\Downloads\del" --target-pdf-size 2`

