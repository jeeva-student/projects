import requests
from bs4 import BeautifulSoup
import pdfkit
import subprocess


class HeadingsExtractor:
    def __init__(self, urls, output_html, output_pdf, wkhtmltopdf_path):
        self.urls = urls
        self.output_html = output_html
        self.output_pdf = output_pdf
        self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    def fetch_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  
            return response.content
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_headings_and_links(self):
        headings_and_links = ''
        for url in self.urls:
            print(f"Processing URL: {url}")
            content = self.fetch_content(url)
            if not content:
                continue
            
            soup = BeautifulSoup(content, 'html.parser')
            for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                heading_text = heading.get_text(strip=True)
                a_tag = heading.find('a')
                if a_tag and a_tag.get('href'):
                    link = a_tag['href']
                    full_link = link if link.startswith('http') else f"https://www.thehindu.com{link}"
                    headings_and_links += f"Heading: {heading_text}\nLink: {full_link}\n\n"
        
        return headings_and_links
    
    def save_to_html(self, content):
        if not content.strip():
            print("No content to save in HTML.")
            return
        html_content = f"<html><body><pre>{content}</pre></body></html>"
        with open(self.output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML file saved to {self.output_html}")

    """def save_to_html(self, content):
        html_content = f"<html><body><pre>{content}</pre></body></html>"
        with open(self.output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML file saved to {self.output_html}")"""

    def debug_wkhtmltopdf(self):
        command = f'"{self.config.wkhtmltopdf}" "{self.output_html}" "{self.output_pdf}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"wkhtmltopdf failed:\n{result.stderr}")
            raise OSError(f"wkhtmltopdf failed with error:\n{result.stderr}")

    def generate_pdf(self):
        options = {
            'disable-smart-shrinking': '',
            'enable-local-file-access': '',
            'quiet': '',
            'no-stop-slow-scripts': '',
            'disable-gpu': ''
        }
        try:
            pdfkit.from_file(self.output_html, self.output_pdf, configuration=self.config, options=options)
            print(f"PDF saved successfully to {self.output_pdf}")
        except OSError as e:
            print(f"Error during PDF generation: {e}")
            self.debug_wkhtmltopdf()

    def process(self):
        headings_and_links = self.extract_headings_and_links()
        self.save_to_html(headings_and_links)   
        self.generate_pdf()


"""# Main execution
if __name__ == "__main__":
    urls = [
        'https://www.thehindu.com/todays-paper/', 'https://www.thehindu.com/sport/olympics/',
        'https://www.thehindu.com/sport/cricket/', 'https://www.thehindu.com/sport/football/',
        'https://www.thehindu.com/sport/hockey/', 'https://www.thehindu.com/sport/tennis/',
        'https://www.thehindu.com/sport/athletics/', 'https://www.thehindu.com/sport/motorsport/',
        'https://www.thehindu.com/sport/other-sports/', 'https://www.thehindu.com/business/agri-business/',
        'https://www.thehindu.com/business/Economy/', 'https://www.thehindu.com/business/Industry/',
        'https://www.thehindu.com/business/markets/', 'https://www.thehindu.com/business/budget/',
        'https://www.thehindu.com/sci-tech/science/', 'https://www.thehindu.com/sci-tech/technology/',
        'https://www.thehindu.com/sci-tech/health/', 'https://www.thehindu.com/sci-tech/agriculture/',
        'https://www.thehindu.com/sci-tech/energy-and-environment/', 
        'https://www.thehindu.com/sci-tech/technology/gadgets/',
        'https://www.thehindu.com/sci-tech/technology/internet/'
    ]

    output_html = 'headings_and_links.html'
    output_pdf = 'headings_and_links.pdf'
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    # Create an instance of HeadingsExtractor and process the URLs
    extractor = HeadingsExtractor(urls, output_html, output_pdf, wkhtmltopdf_path)
    extractor.process()"""



# collect_head_link.py
import requests
from bs4 import BeautifulSoup
import pdfkit

# Set up the path to wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')


class HeadLinkCollector:
    def __init__(self, url):
        self.url = url

    def collect_headings_and_links(self):
        #config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        headings_and_links = ''
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = heading.get_text()
            a_tag = heading.find('a')
            if a_tag and a_tag.get('href'):
                link = a_tag['href']
                full_link = link if link.startswith('http') else f"https://www.thehindu.com{link}"
                headings_and_links += f"Heading: {heading_text}\nLink: {full_link}\n\n"
        return headings_and_links

    def save_to_html_and_pdf(self, headings_and_links, html_path, pdf_path):
        html_content = f"<html><body><pre>{headings_and_links}</pre></body></html>"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        pdfkit.from_file(html_path, pdf_path, configuration=config)  # Use the config
        print(f"PDF with headings and links saved to {pdf_path}")


#this works good but iam trying to do in class
"""import requests
from bs4 import BeautifulSoup
import pdfkit

# Set up the path to wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

url = 'https://www.thehindu.com/todays-paper/'

# Fetch the webpage content
response = requests.get(url)

# Parse the webpage content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract headings and href links
headings_and_links = ''
for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    heading_text = heading.get_text()
    
    # Find the first anchor tag within the heading if it exists
    a_tag = heading.find('a')
    if a_tag and a_tag.get('href'):
        link = a_tag['href']
        full_link = link if link.startswith('http') else f"https://www.thehindu.com{link}"  # Convert relative to absolute URL
        
        # Append the heading text and corresponding link to the string
        headings_and_links += f"Heading: {heading_text}\nLink: {full_link}\n\n"

# Save the extracted headings and links as an HTML file (pdfkit will use this to generate the PDF)
html_content = f"<html><body><pre>{headings_and_links}</pre></body></html>"

with open('headings_and_links_1.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Convert the HTML file to PDF using pdfkit
pdfkit.from_file('headings_and_links_1.html', 'headings_and_links_1.pdf', configuration=config)

print("PDF with headings and links saved successfully!")"""