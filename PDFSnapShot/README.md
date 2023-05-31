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
snapshots of each page of PDF files. 

It can also iterate over all PDF files in given directories, including nested their 
sub-folders, and uses the `pdf2image` package to convert PDF pages to JPEG images.

**Notes:**
1. Each generated JPEG image is named with the original PDF file name and the corresponding page number.
2. If user does not specify the destination directory path, then the output directory, `pdf-snapshots`, 
is created automatically **within the source directory** of each PDF file.

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
    ├── pdf_file_1.pdf  <== Has one page only
    ├── pdf_file_2.pdf  <== Has two pages
    ├── pdf-snapshots   <== Default Destination Directory of Generated images
    │   ├── pdf_file_1-page-1.jpg
    │   ├── pdf_file_2-page-1.jpg
    │   └── pdf_file_2-page-2.jpg
    ├── subdirectory
    │   ├── subdirectory_pdf.pdf  <== Has one page only
    │   └── pdf-snapshots         <== Default Destination Directory of Generated images
    │       └── subdirectory_pdf-page-1.jpg
    └── ...
```

By executing this application, you can conveniently generate a series of screenshots 
that correspond to each page of the PDF files that are either a PDF itself or reside 
in the specified directories . This can be useful for various purposes such as 
archiving, visual reference, or further analysis of the PDF content.


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
### 5.1. Explanation:
Suppose you have the following directories where your PDF files are stored:
```text
C:
└── Documents
    ├── DOC_PDF1.pdf
    ├── DOC_PDF2.pdf
    └── DOC_PDF3.pdf

D:
└── Files
    ├── File_PDF1.pdf
    └── File_PDF2.pdf
```

Now, suppose you want to use this tool on directory (C:\Document) on also on a specific 
PDF file (D:\Files\File_PDF1.pdf). In this case, run this application with `--input-paths` 
and provide the Directory and PDF file paths separated by comma.
<br />

```python pdf_snapshot.py --input-paths "<path_to_pdfs>, <path_to_directories>" --dest-path "<path_to_destination_directory>"```

* Replace `<path_to_pdfs>` with the actual path to your PDF files separated by comma.
* Replace `<path_to_directories>` with the actual path to the directories containing 
your PDF files separated by comma.
* Optionally, User can also use `--dest-path` to specify a destination directory where 
the generated snapshots must be stored. If this optional argument is not provided then
generated snapshots will be saved in an output directory called `pdf-snapshots` which 
is automatically created **within the source directory** of each PDF file. If user wants
to specify a destination directory to store generated snapshots in a single place, they 
should replace `<path_to_destination_directory>` with the actual path of the destination
directory. 

**Note:** Please put arguments of both `--input-paths` and `--dest-path` inside a 
single/double quote.

### 5.1. Example:

Open the command prompt (CMD) or PowerShell, navigate to the directory where this code repository is 
located, and execute the following command depending on your need:
* `cd automated-Life` <br /> 
* `python PDFSnapShot/run.py --input_dirs "C:\Document,D:\Files\Sample.PDF"`

## 6. Contributions
Contributions to this project are welcome! If you encounter any issues or have 
suggestions for improvements, please open an issue or submit a pull request.

Feel free to customize this README file based on your specific project details and 
requirements. Make sure to include relevant information such as any additional setup 
instructions or usage examples specific to your application.
