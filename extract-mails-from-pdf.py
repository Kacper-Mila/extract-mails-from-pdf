import PyPDF2
import re
import os
from pdf2image import convert_from_path
import pytesseract
from utils import colors

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
not_accepted_domain_patterns = [
    r"\b[A-Za-z0-9._%+-]+@revvity.com\b",
    r"\b[A-Za-z0-9._%+-]+@perkinelmer.com\b",
]


def get_pdf_files(folder_path):
    try:
        print("Getting pdf files")
        pdf_files = []
        
        if len([name for name in os.listdir(folder_path) if name.endswith(".pdf")]) == 0:
            raise Exception("No pdf files found")
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
        
        print(f"{colors.BLUE}Found {len(pdf_files)} pdf files{colors.END}")
        
        return pdf_files
    
    except Exception as e:
        print(f"{colors.RED}Error getting pdf files: {e}{colors.END}")
        return []


def get_text_from_scanned_pdf(pdf_file):
    images = convert_from_path(pdf_file)
    text = ""
    for i in range(len(images)):
        text += pytesseract.image_to_string(images[i])
    return text


def extract_emails(pdf_files):
    emails = []
    for file in pdf_files:
        print(f"{colors.BLUE}Extracting emails from file: {os.path.basename(file)}{colors.END}")
        try:
            with open(file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_num in range(len(reader.pages)):
                    print(f"Page {page_num + 1}/{len(reader.pages)}")
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if not text:
                        if page_num == 0:
                            print(f"{colors.YELLOW}Converting scanned pdf, it can take a bit longer{colors.END}")
                        text = get_text_from_scanned_pdf(file)
                    found_emails = re.findall(email_pattern, text)
                    for email in found_emails:
                        if email.lower() not in [e[0] for e in emails]:
                            emails.append((email.lower(), os.path.basename(file)))
        except Exception as e:
            print(
                f"{colors.RED}Error extracting emails from {os.path.basename(file)}: {e} {colors.END}"
            )

    return emails


def write_to_csv(emails, folder_path):
    print("Generating csv file")
    os.makedirs(folder_path, exist_ok=True)
    with open(os.path.join(folder_path, "emails.csv"), "w+") as f:
        f.write("Emails,found in\n")
        for email in emails:
            if not re.match(not_accepted_domain_patterns[0], email[0]) and not re.match(
                not_accepted_domain_patterns[1], email[0]
            ):
                f.write(f"{email[0]},{email[1]}\n")


def main():
    print("Enter the folder path (Example: C:/Users/<USERNAME>/Documents/)")
    folder_path = input(">> ")

    pdf_files = get_pdf_files(folder_path)
    
    if not pdf_files:
        return
    
    emails = extract_emails(pdf_files)
    write_to_csv(emails, folder_path)

    print(f"{colors.GREEN}Done{colors.END}")
    print(f"{colors.GREEN}Emails are saved in {folder_path}/emails.csv{colors.END}")


if __name__ == "__main__":
    main()
