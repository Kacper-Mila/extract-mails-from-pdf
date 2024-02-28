# Email Extractor from PDF

Extract every email address from PDF files. For scanned files, it converts every page into a photo, then uses Tesseract to extract text from the photo.

## Prerequisites

~~The program can extract text from almost every PDF file, but for photos or some scanned files, you'll need to install Tesseract. Follow the instructions [here](https://github.com/UB-Mannheim/tesseract/wiki) to install it. Place Tesseract in `C:\Program Files` on Windows or edit `extract-mails-from-pdf.py`:~~

Tesseract and Poppler files are included in the resources directory. But if any problems occur with Tesseract, please download it from [here](https://github.com/UB-Mannheim/tesseract/wiki). And change the path to it in extract-mails-from-pdf.py:

```python
pytesseract.pytesseract.tesseract_cmd = r"PATH/TO/Tesseract-OCR/tesseract.exe"
 ```
## How to use
1. Build an exe with: 
```
pyinstaller --noconfirm --onedir --console --add-data "C:/Users/kacpe/Documents/Programming/Python/extract-mails-from-pdf/resources;resources/"  "C:/Users/kacpe/Documents/Programming/Python/extract-mails-from-pdf/extract-mails-from-pdf.py"
```  
or run it from command line.

2. Then, provide the path to the folder containing the PDF files. The program will scan every PDF file in this directory.

3. After a few seconds, a CSV file will be generated containing every email found and the corresponding file in which it was found. (Duplicates of email addresses are removed.)

### Ignore domains
You can add domains to ignore in `utils.py`.
```
ignored_domains = [
    r"@gmail.com\b",
    r"@yahoo.com\b"
]
```
