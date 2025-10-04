This app is about converting a PDF into a black and white version of it.

---

## 1. How does the need arised?
06 Jan 2025: Someone asked passport bio pages and I didn't want to share the color passport. If they have ot have it, why give them an exact relica: Make it a little bit difficult for them to misuse.

I know it can be done manually within minutes. But there're too many and it never stops. It's not pleasant.

So this is what this app does: It takes a PDF and create a copy but each pages will be turn into B&W version of it. The size of generated PDF must always be less the original. Ideally make the size as low as possible without reducing quality.

So idea is this: Turn a PDF or collection of PDFs into it's B&W version

---
## 2. How to run the application:

* `cd automated-Life` <br /> 
* `python turnPdfBW/run.py --input-paths "/Users/UserName/Downloads/"`

## 2. One-time installation

1. Install all Python packages with: `pip install -r turnPdfBW/requirements.txt`
2. Poppler (System Library): `poppler` is not a Python package, so it must be installed separately depending on your OS. Look at Section 2.1.


### 2.1. How to  Install Poppler (System Library)

**2.1.1. Windows:**
1. Download Poppler: [https://github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Extract the ZIP to a folder, e.g., `C:\poppler`.
3. Add the `bin` folder (e.g., `C:\poppler\Poppler-23.06.0-0\bin`) to your **PATH**.
4. Restart your terminal/IDE.

**Tip:**
On Windows, if you don’t set the PATH, `pdf2image` will throw an error like:

```
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

You **must** set the PATH or provide `poppler_path` explicitly in your script:

```python
from pdf2image import convert_from_path
pages = convert_from_path("input.pdf", poppler_path=r"C:\poppler\Poppler-23.06.0-0\bin")
```

**2.1.2. Mac:**
```bash
brew install poppler
```

* **No need to manually set PATH** if installed via package manager (`brew install poppler`), because the binaries are already in standard system paths.

**2.1.3. Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install poppler-utils
```

---


### 3. Verify Poppler Installation

```bash
pdftoppm -h
```
You should see the Poppler help message. Once this works, your PDF-to-black-and-white script will run successfully.



