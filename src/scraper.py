import requests
from bs4 import BeautifulSoup
import os

# URL of the Florida Revenue Delinquent Taxpayer page
PAGE_URL = "https://floridarevenue.com/taxes/compliance/Pages/delinquent_taxpayer.aspx"

# Folder to save downloaded Excel
DATA_DIR = "../tax-lien-demo/data"  # adjust relative path if needed
os.makedirs(DATA_DIR, exist_ok=True)

def get_excel_link(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Look for <a> tags with .xls or .xlsx
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        if href.endswith(".xls") or href.endswith(".xlsx"):
            # Convert relative URL to absolute
            if href.startswith("http"):
                return href
            else:
                return "https://floridarevenue.com" + href
    return None

def download_excel(url, save_folder):
    file_name = url.split("/")[-1]
    file_path = os.path.join(save_folder, file_name)
    
    r = requests.get(url)
    r.raise_for_status()
    
    with open(file_path, "wb") as f:
        f.write(r.content)
    print(f"Excel downloaded successfully: {file_path}")
    return file_path

if __name__ == "__main__":
    excel_url = get_excel_link(PAGE_URL)
    if excel_url:
        download_excel(excel_url, DATA_DIR)
    else:
        print("No Excel link found on the page.")
