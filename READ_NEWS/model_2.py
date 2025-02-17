import pdfplumber
import pandas as pd
from fpdf import FPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def extract_pdf_content(pdf_path):
    headings_and_contents = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split("\n")
                heading, content = None, []
                for line in lines:
                    if line.startswith("Heading:"):
                        if heading:
                            # Append the previous heading and content
                            headings_and_contents.append((heading, " ".join(content)))
                        heading = line.replace("Heading:", "").strip()
                        content = []
                    elif line.startswith("Content:"):
                        continue
                    else:
                        content.append(line.strip())
                # Append the last heading and content
                if heading:
                    headings_and_contents.append((heading, " ".join(content)))
    return headings_and_contents

def train_nlp_model(csv_path):
    data = pd.read_csv(csv_path)
    X = data['Text']  # Assuming the text column is named 'Text'
    y = data['Category']  # Assuming the label column is named 'Category'
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build a pipeline
    model = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', MultinomialNB(alpha=0.1))
    ])
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return model

def classify_headings(model, headings_and_contents):
    classified_data = {}
    for heading, content in headings_and_contents:
        category = model.predict([heading])[0]
        if category not in classified_data:
            classified_data[category] = []
        classified_data[category].append((heading, content))
    return classified_data

def save_to_pdf(classified_data, output_pdf_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for category, entries in classified_data.items():
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, category, ln=True, align='C')
        
        for heading, content in entries:
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"Heading: {heading}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"Content: {content}\n")
    
    pdf.output(output_pdf_path)
    print(f"Classified PDF saved to {output_pdf_path}")

if __name__ == "__main__":
    # Step 1: Extract data from PDF
    pdf_path = "C://Users//LENOVO//jeeva//news//cleaned_output.pdf"
    headings_and_contents = extract_pdf_content(pdf_path)
    
    # Step 2: Train the NLP model
    csv_path = "C://Users//LENOVO//jeeva//news//BBCNewsTrain//BBC_News_Train.csv"
    model = train_nlp_model(csv_path)
    
    # Step 3: Classify headings
    classified_data = classify_headings(model, headings_and_contents)
    
    # Step 4: Save classified data to a new PDF
    output_pdf_path = "classified_output.pdf"
    save_to_pdf(classified_data, output_pdf_path)