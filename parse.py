from bs4 import BeautifulSoup
import PyPDF2
import docx
import xml.etree.ElementTree as ET
import pandas as pd

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.find_all("table")
    paragraphs = soup.find_all("p")

    table_text = ""
    for table in tables[:2]:
        table_text += table.get_text(separator=" ", strip=True) + "\n\n"

    para_text = ""
    for para in paragraphs[:5]:
        para_text += para.get_text(strip=True) + "\n\n"

    combined = para_text + table_text

    # Fallback: If nothing found in <p> or <table>, grab all visible text
    if not combined.strip():
        combined = soup.get_text(separator="\n", strip=True)

    return combined[:3000]  # Limit size for context safety

def parse_document(file, file_type):
    content = ""

    if file_type == "pdf":
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content += page.extract_text() + "\n"

    elif file_type == "docx":
        doc = docx.Document(file)
        for para in doc.paragraphs:
            content += para.text + "\n"

    elif file_type == "xml":
        tree = ET.parse(file)
        root = tree.getroot()
        content += ET.tostring(root, encoding='unicode', method='text')

    elif file_type == "csv":
        df = pd.read_csv(file)
        content += df.to_string(index=False)

    else:
        content = "Unsupported file type."

    return content
