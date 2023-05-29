## 1. PDF Snapshot Application:
```
............
.          .
.   PDF    .
. Snapshot .
.          .
............
```
The **PDF Snapshot** is a Python application that allows you to generate JPEG 
snapshots of each page of a PDF file. 

It iterates over all PDF files in a given directory, including nested subfolders, and 
uses the `pdf2image` package to convert PDF pages to JPEG images.

**Notes:**
1. Each generated JPEG image is named with the original PDF file name and the corresponding page number.
2. The output directory, `pdf-snapshots`, is created automatically **within the input directory**.

## 2. How Does This Tool Work?
The provided Python application iterates over all PDF files in a given directory and 
captures a screenshot of each page within the PDF. 

If a PDF contains multiple pages, each screenshot is saved with a filename that 
includes the original file name and the page number. Please note that each generated 
image is stored in the same location as the source PDF file, within a directory named "pdf-snapshots".  

Once execution completes, this will be the final structure of each directory
inside user-given input directories.
```
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
```

By executing this application, you can conveniently generate a series of screenshots 
that correspond to each page of the PDF files in the specified directory. This can be 
useful for various purposes such as archiving, visual reference, or further analysis of 
the PDF content.


## 3. Prerequisites
* Python 3.6 or higher

## 4. Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.

### 4.1. Setting up Dependencies

Install the Python dependencies by running the following command:<br />
```pip install -r requirements.txt```<br /><br />
 
### 4.2. Issue with PDFInfoNotInstalledError (How to Resolve)
**Windows users might encounter the PDFInfoNotInstalledError.** In such cases, 
please follow the instructions below:

* Download the latest stable release of Poppler for Windows from the following link: https://poppler.freedesktop.org/
* Extract the contents of the downloaded ZIP file to a location on your computer.
* Add the path to the extracted Poppler binaries (e.g., `C:\path\to\poppler\bin`) to the system's PATH environment variable.


The application uses `pdf2image` that in turns requires certain dependencies to be 
installed. and accessible in the system's PATH for it to work correctly.

If you're encountering the PDFInfoNotInstalledError, it means that Poppler is not 
properly installed or not found in the PATH environment variable.

To resolve this issue, you need to install Poppler and ensure it is accessible in the 
PATH. Here are the steps to do so:

**For Windows:**
1. Download the pre-built Poppler binaries for Windows from the official repository: https://github.com/oschwartz10612/poppler-windows/releases
3. Extract the contents of the downloaded archive.
4. Add the `bin` path of the extracted Poppler binaries (e.g., `C:\path\to\poppler\bin`) to 
the system's PATH environment variable. <br /> In Mantosh's Windows system, the bin direcory of Poppler package is `C:\manu-custom-package-installs\poppler-23.05.0\Library\bin`

**For macOS:**
1. Install Poppler using Homebrew by running the following command in the terminal: ```brew install poppler```

**For Linux:**
1. Install Poppler using the package manager for your specific Linux distribution. 
For example, on Ubuntu, you can use the following command:
```sudo apt-get install poppler-utils```

Please note that if you are using a Linux system then this dependency is already 
taken care of if you have already used `requirements.txt` to install dependencies.

## 5. How To Use This Tool:
### 5.1. If Only Need To Do The Task:
Suppose you have the following directories where your PDF files are stores:
* C:\Documents\Directory1
* C:\Files\Directory2
* D:\Projects\Directory3

To run the application and provide these directories as input separated by comma, open the command 
prompt (CMD) or PowerShell, navigate to the directory where this code repository is 
located, and execute the following command:

`cd automated-Life`

`python PDFSnapShot/run.py --input_dirs "C:\Documents\Directory1,C:\Files\Directory2,D:\Projects\Directory3"`

### 5.2. If Need To Use This Tool Programmatically:
1. Place your PDF files in a directory. 
2. Run the application by executing the following command:<br />
```python pdf_snapshot.py --input_dir <path_to_directory>```
    <br /><br />
    Replace `<path_to_directory>` with the actual path to the directory containing your PDF files.<br />
    <br />
    **Note:** The application will generate a snapshot for each page of every PDF file found in the specified directory.

3. The generated snapshots will be saved in the output directory within the project.


## 6. Contributions
Contributions to this project are welcome! If you encounter any issues or have 
suggestions for improvements, please open an issue or submit a pull request.

Feel free to customize this README file based on your specific project details and 
requirements. Make sure to include relevant information such as any additional setup 
instructions or usage examples specific to your application.







