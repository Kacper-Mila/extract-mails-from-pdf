import PyPDF2
import re
import os
import sys
from pdf2image import convert_from_path
import pytesseract
from utils import colors, email_pattern, ignored_domains

# Set Poppler and Tesseract path
# Check if we're running as a PyInstaller bundle
if getattr(sys, "frozen", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

_poppler_path = os.path.join(
    base_path, "resources", "Poppler-24.02.0-0", "poppler-24.02.0", "Library", "bin"
)
_tesseract_path = os.path.join(base_path, "resources", "Tesseract-OCR", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = _tesseract_path


def get_pdf_files(folder_path):
    try:
        print("Getting pdf files")
        pdf_files = []

        if (
            len([name for name in os.listdir(folder_path) if name.endswith(".pdf")])
            == 0
        ):
            raise Exception("No pdf files found")

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))

        print(f"{colors.INFO + colors.BOLD}Found {len(pdf_files)} pdf files{colors.END}")

        return pdf_files

    except Exception as e:
        print(f"{colors.DANGER}Error getting pdf files: {e}{colors.END}")
        return []


def get_text_from_scanned_pdf(pdf_file):
    images = convert_from_path(pdf_file, poppler_path=_poppler_path)
    text = ""
    for i in range(len(images)):
        text += pytesseract.image_to_string(images[i])
    return text


def extract_emails(pdf_files):
    emails = []
    for file in pdf_files:
        print(
            f"{colors.INFO + colors.BOLD}Extracting emails from file: {os.path.basename(file)}{colors.END}"
        )
        try:
            with open(file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_num in range(len(reader.pages)):
                    print(f"Page {page_num + 1}/{len(reader.pages)}")
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if not text:
                        if page_num == 0:
                            print(
                                f"{colors.WARNING}Converting scanned pdf, it can take a bit longer{colors.END}"
                            )
                        text = get_text_from_scanned_pdf(file)
                    found_emails = re.findall(email_pattern, text)
                    for email in found_emails:
                        if email.lower() not in [e[0] for e in emails]:
                            emails.append((email.lower(), os.path.basename(file)))
        except Exception as e:
            print(
                f"{colors.DANGER}Error extracting emails from {os.path.basename(file)}: {e} {colors.END}"
            )

    return emails


def remove_ignored_domains(emails):
    mails_to_remove = []
    for email in emails:
        for domain in ignored_domains:
            if re.search(domain, email[0]):
                mails_to_remove.append(email)
                break
            
    for mail in mails_to_remove:
        emails.remove(mail)
        
    return emails


def write_to_csv(emails, folder_path):
    print("Generating csv file")
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, "emails.csv"), "w+") as f:
        f.write("Emails,found in\n")
        for email in emails:
            f.write(f"{email[0]},{email[1]}\n")


def main():
    print("Enter the folder path (Example: C:/Users/<USERNAME>/Documents/)")
    folder_path = input(">> ")

    pdf_files = get_pdf_files(folder_path)

    if not pdf_files:
        return

    emails = extract_emails(pdf_files)
    filtered_emails = remove_ignored_domains(emails)
    write_to_csv(filtered_emails, folder_path)

    print(f"{colors.SUCCESS}Done{colors.END}")
    print(f"{colors.SUCCESS}Emails are saved in {folder_path}/emails.csv{colors.END}")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
