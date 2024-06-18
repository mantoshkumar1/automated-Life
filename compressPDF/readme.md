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

## 2. How to Use this Application?
* `cd automated-Life` <br /> 
* `python compressPDF\run.py --input-paths "C:\Users\MANTKUMAR\Downloads\delete" --dest-dir="C:\Us
ers\MANTKUMAR\Downloads\del" --target-pdf-size 2`

**usage: run.py [-h] --input-paths INPUT_DIRS [--dest-dir DEST_DIR] --target-pdf-size TARGET_PDF_SIZE (in MB)**

* `input-paths` is a mandatory string field. Provide the directory path that contains your PDF files. You can also specify PDF file paths. Just make sure that they are separated by comma. The whole input should be a string.
* `dest-dir` is an optional string field. If you do not use this argument then the reduced sized PDF file gets stored in the same directory where the original PDF is stored. The name of the reduced sized PDF will start with `compressed-originalFileName.pdf`
* `target-pdf-size` is a mandatory integer field. This argument specifies your desired size of PDF in MB.


### 3. How to Setup Dependencies:
* Python 3.6 or higher
* Install the Python dependencies by running the following command:<br />
```pip install -r requirements.txt```<br />
