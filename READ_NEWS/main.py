from collect_head_content import HeadContentCollector  # From collect_head_content.py
from collect_head_link import HeadingsExtractor  # From collect_head_link.py
from head_content_clean import PDFContentCleaner  # From head_content_clean.py

def main():
    
    # Step 2: Extract headings and links from URLs and save as HTML and PDF
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
        'https://www.thehindu.com/sci-tech/energy-and-environment/', 'https://www.thehindu.com/sci-tech/technology/gadgets/',
        'https://www.thehindu.com/sci-tech/technology/internet/','https://www.thehindu.com/news/national/'
    ]
    output_html = 'headings_and_links.html'
    output_pdf = 'headings_and_links.pdf'
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    link_extractor = HeadingsExtractor(urls, output_html, output_pdf, wkhtmltopdf_path)
    link_extractor.process()

        # Step 1: Extract headings and links from a PDF
    pdf_path = 'headings_and_links.pdf'  # Input PDF with headings and links
    output_pdf_path = 'final_headings_and_content.pdf'  # Output PDF with content
    content_collector = HeadContentCollector()
    headings_and_links = content_collector.extract_headings_and_links_from_pdf(pdf_path)
    content_collector.save_headings_and_content_to_pdf(headings_and_links, output_pdf_path)

    # Step 3: Clean a PDF by removing unwanted words
    input_pdf_clean = output_pdf_path  # Use the PDF generated from Step 1
    output_pdf_clean = 'cleaned_final_output.pdf'
    pdf_cleaner = PDFContentCleaner()
    pdf_cleaner.process_pdf(input_pdf_clean, output_pdf_clean)

if __name__ == "__main__":
    main()



"""# main.py
from collect_head_content import HeadContentCollector
from collect_head_link import HeadLinkCollector
from head_content_clean import PDFContentCleaner

# Using the classes in your main Python script
if __name__ == "__main__":
    
    # Example usage of HeadLinkCollector
    link_collector = HeadLinkCollector('https://www.thehindu.com/todays-paper/')
    links = link_collector.collect_headings_and_links()
    link_collector.save_to_html_and_pdf(links, 'headings_and_links.html', 'headings_and_links.pdf')

    # Example usage of HeadContentCollector
    collector = HeadContentCollector()
    headings_and_links = collector.extract_headings_and_links_from_pdf('headings_and_links.pdf')
    collector.save_headings_and_content_to_pdf(headings_and_links, 'output_collected.pdf')

    # Example usage of PDFContentCleaner
    cleaner = PDFContentCleaner()
    cleaner.process_pdf('output_collected.pdf', 'cleaned_output.pdf')"""
