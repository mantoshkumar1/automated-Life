# Image2PDF Converter

## What it Does:
Image2PDF Converter is a Python application that first numerically sorts the "jpg"
images in a particular folder and then merge them into a single PDF document. 

This PDF can either be stored at user specified target folder or in the source folder 
itself if target folder is not mentioned. The name of the resulting PDF will be "merged_images_into_pdf"

This application simplifies the task of organizing and sharing image files by creating 
a unified PDF file from a collection of JPEGs.

## How to Use it:
1. In Windows, to install `reportlab` python package you first need to install Microsoft Visual C++ 14.0 or greater. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/ (Choose the "Desktop Development with C++" option while installing).
2. Install the required dependencies: PIL (Python Imaging Library) and reportlab.
    
    ```pip install -r image2Pdf/requirements.txt```

3. Run the script with the input folder containing JPEG images and specify the output PDF file.

   ```python image2Pdf\run.py --input-path "C:\Source_Folder"  --dest-dir "C:\Dest_Folder"```

   Note: `--input-path` is a mandatory field.
   Note: `--dest-dir` is an optional field.

   If you do not specify output directory then the resulting PDF
   ("merged_images_into_pdf.pdf") will be stored in the same directory as the source directory.

   Note: Keep the filenames like this for correct ordering of pages: 'characters-digit' or 
   simply 'digits'. For example: 'file1.jpg, file2.jpg' or simply as '1.jpg, 2.jpg' 
   TODO: This could be made better like Windows OS sorts filename by its character. Look into function "utility/file_functions.py/sort_filenames_numerically". Improve it.

## Motivation:
The motivation behind Image2PDF Converter was the need for a convenient solution to merge multiple JPEG images into a standardized and shareable format. By providing a simple yet powerful tool, we aim to streamline the process of managing image files and enhance productivity for individuals and businesses alike.

## How it Works:
1. The script iterates through the input folder containing JPEG images.
2. Each image is resized to fit the page width of the PDF document.
3. The resized images are sequentially added to the PDF document.
4. The resulting PDF document contains all the input images merged into a single file.

## Benefits:
- *Convenience*: Merge multiple JPEG images into a single PDF document with a single command.
- *Efficiency*: Simplify the task of organizing and sharing image files.
- *Customization*: Resize images to fit the page width of the PDF document.
- *Productivity*: Enhance productivity for individuals and businesses dealing with a large number of image files.

# Future TODO:
* 10 June 2024: As of now, it only handles jpg images. Make it work with all kind of images.

## Requirements:
- Python 3.x
- PIL (Python Imaging Library)
- reportlab

## Contributors:
- Mantosh Kumar

## License:
This project is licensed under the [MIT License](LICENSE).
