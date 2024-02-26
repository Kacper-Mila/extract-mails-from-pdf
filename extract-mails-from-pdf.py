import PyPDF2
import re
import os
from pdf2image import convert_from_path
import pytesseract


email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
not_accepted_domain_patterns = [
    r"\b[A-Za-z0-9._%+-]+@revvity.com\b",
    r"\b[A-Za-z0-9._%+-]+@perkinelmer.com\b",
]


def get_pdf_files(folder_path):
    print("Getting pdf files")
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


    
def get_text_from_scanned_pdf(pdf_file):
    print(f"Extracting text from scanned pdf: {pdf_file}")
    images = convert_from_path(pdf_file)
    text = ""
    for i in range(len(images)):
        text += pytesseract.image_to_string(images[i])
    return text


def extract_emails(pdf_files):
    emails = []
    for file in pdf_files:
        print(f"Extracting emails from pdf file: {os.path.basename(file)}")
        with open(file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                found_emails = re.findall(email_pattern, text)
                for email in found_emails:
                    emails.append((email, os.path.basename(file)))  # get the file name, not the path
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
    emails = extract_emails(pdf_files)
    write_to_csv(emails, folder_path)

    print("Done")
    print(f"Emails are saved in {folder_path}/emails.csv")


if __name__ == "__main__":
    main()
