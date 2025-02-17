# collect_head_content.py
import requests
from bs4 import BeautifulSoup
import PyPDF2
from fpdf import FPDF
import unicodedata

class HeadContentCollector:
    def extract_headings_and_links_from_pdf(self, pdf_path):
        headings_and_links = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    for i in range(len(lines)):
                        if lines[i].startswith("Heading:"):
                            heading = lines[i].replace("Heading:", "").strip()
                            if i + 1 < len(lines) and lines[i + 1].startswith("Link:"):
                                link = lines[i + 1].replace("Link:", "").strip()
                                headings_and_links.append((heading, link))
        return headings_and_links

    def extract_content_from_link(self, link):
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('div', id='content-body-')  # Replace with correct ID/tag
            if content:
                return content.get_text(separator='\n', strip=True)
        except Exception as e:
            print(f"Failed to retrieve content from {link}: {e}")
            return None

    def remove_special_characters(self, text):
        text = unicodedata.normalize('NFKD', text)
        return text.encode('latin1', 'ignore').decode('latin1')

    def save_headings_and_content_to_pdf(self, headings_and_links, output_pdf_path):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for heading, link in headings_and_links:
            if heading:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                heading = self.remove_special_characters(heading)
                pdf.multi_cell(0, 10, f"Heading: {heading}")
                pdf.set_font("Arial", size=12)
                content = self.extract_content_from_link(link)
                if content:
                    content = self.remove_special_characters(content)
                    pdf.multi_cell(0, 10, f"Content:\n{content}\n")
                else:
                    pdf.multi_cell(0, 10, "Content: Content could not be retrieved.\n")
        pdf.output(output_pdf_path)
        print(f"PDF with headings and content saved to {output_pdf_path}")



#this works good but iam trying to do in class
"""import requests
from bs4 import BeautifulSoup
import PyPDF2
from fpdf import FPDF
import unicodedata

# Function to read the uploaded PDF and extract headings and links
def extract_headings_and_links_from_pdf(pdf_path):
    headings_and_links = []
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for i in range(len(lines)):
                    if lines[i].startswith("Heading:"):
                        heading = lines[i].replace("Heading:", "").strip()
                        if i + 1 < len(lines) and lines[i + 1].startswith("Link:"):
                            link = lines[i + 1].replace("Link:", "").strip()
                            headings_and_links.append((heading, link))
    
    return headings_and_links

# Function to visit each link and extract the main content
def extract_content_from_link(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Adjust this selector to match the main content of the webpage
        content = soup.find('div', id='content-body-')  # Replace with the correct ID/tag
        if content:
            return content.get_text(separator='\n', strip=True)
    except Exception as e:
        print(f"Failed to retrieve content from {link}: {e}")
        return None  # Return None if the content could not be retrieved

def remove_special_characters(text):
    # Normalize text to NFC form and remove characters that are not supported by Latin-1
    text = unicodedata.normalize('NFKD', text)
    return text.encode('latin1', 'ignore').decode('latin1')

# In the save_headings_and_content_to_pdf function, modify the content as follows:
def save_headings_and_content_to_pdf(headings_and_links, output_pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)  # Use a standard font like Arial

    for heading, link in headings_and_links:
        if heading:  # Check if heading is not None
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            
            # Write heading and ensure it handles special characters
            heading = remove_special_characters(heading)
            pdf.multi_cell(0, 10, f"Heading: {heading}")
        
            pdf.set_font("Arial", size=12)
            content = extract_content_from_link(link)
            
            if content:  # Check if content is not None
                content = remove_special_characters(content)  # Remove problematic characters from content
                pdf.multi_cell(0, 10, f"Content:\n{content}\n")
            else:
                pdf.multi_cell(0, 10, "Content: Content could not be retrieved.\n")
    
    pdf.output(output_pdf_path)  # No encoding parameter needed
    print(f"PDF with headings and content saved to {output_pdf_path}")

pdf_path = 'C://Users//LENOVO//jeeva//news//headings_and_links_1.pdf'  # Path to your uploaded PDF
headings_and_links = extract_headings_and_links_from_pdf(pdf_path)

output_pdf_path = 'final_headings_and_content.pdf'
save_headings_and_content_to_pdf(headings_and_links, output_pdf_path)"""




"""# Function to create a PDF with headings and their corresponding content
def save_headings_and_content_to_pdf(headings_and_links, output_pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)  # Use a standard font like Arial

    for heading, link in headings_and_links:
        if heading:  # Check if heading is not None
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            
            # Write heading and ensure it handles special characters
            pdf.multi_cell(0, 10, f"Heading: {heading}")
        
            pdf.set_font("Arial", size=12)
            content = extract_content_from_link(link)
            
            if content:  # Check if content is not None
                pdf.multi_cell(0, 10, f"Content:\n{content}\n")
            else:
                pdf.multi_cell(0, 10, "Content: Content could not be retrieved.\n")
    
    pdf.output(output_pdf_path)  # No encoding parameter needed
    print(f"PDF with headings and content saved to {output_pdf_path}")

# Main execution
pdf_path = 'C://Users//LENOVO//jeeva//news//headings_and_links_1.pdf'  # Path to your uploaded PDF
headings_and_links = extract_headings_and_links_from_pdf(pdf_path)

output_pdf_path = 'final_headings_and_content.pdf'
save_headings_and_content_to_pdf(headings_and_links, output_pdf_path)"""