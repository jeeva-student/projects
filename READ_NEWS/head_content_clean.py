import pdfplumber
from fpdf import FPDF

class PDFContentCleaner:
    def __init__(self):
        self.unwanted_words = ["Page No. 1","Page No. 2","Page No. 3", "Page No. 4", "Page No. 5", "Page No. 6", "Page No. 7",
    "Page No. 8","Chennai Print Edition", "SUPPLEMENT", "Main Edition",
    "Page No. 9","Page No. 10", "Copy link", "Email", "Facebook", "Twitter", 
    "Telegram", "LinkedIn", "WhatsApp", "Reddit", "READ LATER", "Remove", "SEE ALL", "PRINT"]

    def is_long_content(self, line):
        return len(line) > 50

    def clean_text(self, lines):
        cleaned_lines = []
        for line in lines:
            if not self.is_long_content(line):
                for word in self.unwanted_words:
                    line = line.replace(word, '')
            cleaned_lines.append(line)
        return cleaned_lines

    def remove_unsupported_characters(self, text):
        return text.encode('latin-1', 'ignore').decode('latin-1')

    def process_pdf(self, input_pdf_path, output_pdf_path):
        pdf_writer = FPDF()
        pdf_writer.set_auto_page_break(auto=True, margin=15)
        pdf_writer.set_font("Arial", size=12)

        with pdfplumber.open(input_pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    cleaned_lines = self.clean_text(lines)
                    cleaned_text = '\n'.join(cleaned_lines)
                    cleaned_text = self.remove_unsupported_characters(cleaned_text)

                    pdf_writer.add_page()
                    pdf_writer.multi_cell(0, 10, cleaned_text)

        pdf_writer.output(output_pdf_path)
        print(f"Cleaned PDF saved to {output_pdf_path}")



#this works good but iam trying to do in class
"""import pdfplumber
from fpdf import FPDF

# List of unwanted words/phrases to remove when not in long content
unwanted_words = ["Page No. 3", "Page No. 4", "Page No. 5", "Page No. 6", "Page No. 7",
    "Page No. 8","Chennai Print Edition", "SUPPLEMENT", "Main Edition",
    "Page No. 9","Page No. 10", "Copy link", "Email", "Facebook", "Twitter", 
    "Telegram", "LinkedIn", "WhatsApp", "Reddit", "READ LATER", "Remove", "SEE ALL", "PRINT"]

# Function to check if a line is part of long content
def is_long_content(line):
    # Adjust this threshold as needed; currently assumes content > 50 characters as "long"
    return len(line) > 50

# Function to clean up extracted text
def clean_text(lines, unwanted_words):
    cleaned_lines = []
    for line in lines:
        # Remove unwanted words if the line is short (not part of long content)
        if not is_long_content(line):
            for word in unwanted_words:
                line = line.replace(word, '')
        cleaned_lines.append(line)
    return cleaned_lines

# Function to extract, clean, and save the PDF content
def process_pdf(input_pdf_path, output_pdf_path):
    pdf_writer = FPDF()
    pdf_writer.set_auto_page_break(auto=True, margin=15)
    pdf_writer.set_font("Arial", size=12)

    with pdfplumber.open(input_pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                cleaned_lines = clean_text(lines, unwanted_words)
                cleaned_text = '\n'.join(cleaned_lines)

                # Add cleaned content to the PDF
                pdf_writer.add_page()
                pdf_writer.multi_cell(0, 10, cleaned_text)

    # Save the new PDF with cleaned content
    pdf_writer.output(output_pdf_path)
    print(f"Cleaned PDF saved to {output_pdf_path}")

# Main execution
input_pdf_path = "C://Users//LENOVO//jeeva//news//final_headings_and_content.pdf"  # Path to your uploaded PDF
output_pdf_path = 'cleaned_final_output.pdf'
process_pdf(input_pdf_path, output_pdf_path)"""
