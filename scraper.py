import requests
from bs4 import BeautifulSoup
from fpdf2 import FPDF
import sys
import os

def fetch_webpage(url):
    try:
        response = requests.get(url)
        # Check for access issues
        if response.status_code in {401, 403, 404, 500, 503}:
            print(f"Error: Cannot access {url}. Status code: {response.status_code}")
            return None
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

def scrape_content(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.get_text()
        return content
    return ""

def save_to_pdf(content, filename):
    from fpdf2 import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to PDF
    pdf.multi_cell(0, 10, content)

    # Save the PDF
    pdf.output(filename)

def process_single(url, output_file):
    print(f"Processing single URL: {url}")
    html = fetch_webpage(url)
    if html:
        content = scrape_content(html)
        save_to_pdf(content, output_file)
        print(f"Content saved to {output_file}")

def process_bulk(urls_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(urls_file, 'r') as file:
        urls = [line.strip() for line in file.readlines()]

    for i, url in enumerate(urls):
        print(f"Processing URL {i + 1}: {url}")
        html = fetch_webpage(url)
        if html:
            content = scrape_content(html)
            pdf_filename = os.path.join(output_dir, f"output_{i + 1}.pdf")
            save_to_pdf(content, pdf_filename)
            print(f"Content saved to {pdf_filename}")
        else:
            print(f"Skipping URL {i + 1} due to access restrictions.")

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("For bulk processing: python scraper.py -b <file_with_urls.txt> <output_directory>")
        print("For single URL: python scraper.py <URL> <output.pdf>")
        sys.exit(1)

    if sys.argv[1] == '-b':
        if len(sys.argv) != 4:
            print("Usage: python scraper.py -b <file_with_urls.txt> <output_directory>")
            sys.exit(1)
        urls_file = sys.argv[2]
        output_dir = sys.argv[3]

        if not os.path.isfile(urls_file):
            print(f"Error: The file {urls_file} does not exist.")
            sys.exit(1)

        process_bulk(urls_file, output_dir)
    else:
        if len(sys.argv) != 3:
            print("Usage: python scraper.py <URL> <output.pdf>")
            sys.exit(1)
        url = sys.argv[1]
        output_file = sys.argv[2]
        process_single(url, output_file)

if __name__ == "__main__":
    main()
