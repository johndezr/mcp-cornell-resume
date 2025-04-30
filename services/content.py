import requests
from bs4 import BeautifulSoup
import pdfplumber
import markdown2

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # solo texto visible
    return soup.get_text(separator="\n")

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

def extract_text_from_markdown(file_path):
    with open(file_path, "r") as f:
        html = markdown2.markdown(f.read())
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")
