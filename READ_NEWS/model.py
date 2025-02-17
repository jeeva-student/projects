import pandas as pd
import re
import pdfplumber
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from fpdf import FPDF
import joblib

"""nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')"""

categories = ['Entertainment', 'Politics', 'Tech', 'Crime', 'Sport']

def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    lemmtizer = WordNetLemmatizer()
    tokens = [lemmtizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def classify_text(text):
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)
    return prediction[0]

def process_and_classify_pdf(input_pdf_path, output_folder_path):
    classified_content = {category: [] for category in categories}

    with pdfplumber.open(input_pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                sections = text.split('\nHeading: ')
                for section in sections[1:]:  # Skip the first part if it's before the first heading
                    parts = section.split('\nContent:', 1)
                    if len(parts) == 2:
                        heading = parts[0].strip()
                        content = parts[1].strip()

                        # Combine heading and content for classification
                        full_text = f"{heading} {content}"
                        category = classify_text(full_text)

                        # Append the content to the respective category
                        classified_content[category].append((heading, content))

    # Save each category to a separate PDF
    for category, entries in classified_content.items():
        if entries:
            pdf_writer = FPDF()
            pdf_writer.set_auto_page_break(auto=True, margin=15)
            pdf_writer.set_font("Arial", size=12)

            for heading, content in entries:
                pdf_writer.add_page()
                pdf_writer.set_font("Arial", 'B', 16)
                pdf_writer.multi_cell(0, 10, f"Heading: {heading}")
                pdf_writer.set_font("Arial", size=12)
                pdf_writer.multi_cell(0, 10, f"Content:\n{content}\n")

            output_path = f"{output_folder_path}/{category}_classified.pdf"
            pdf_writer.output(output_path)
            print(f"PDF for {category} saved to {output_path}")



df1 = pd.read_csv('C:/Users/LENOVO/jeeva/news/BBCNewsTrain/BBC_News_Train.csv')
df2 = df1[['Text','Category']]

df2['clean_headline'] = df2['Text'].apply(preprocess_text)
x = df2['clean_headline']
y = df2['Category']
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)
vectorizer = TfidfVectorizer(max_features=5000)
x_train_tfidf = vectorizer.fit_transform(x_train)
x_test_tfidf = vectorizer.transform(x_test)

model = MultinomialNB()
model.fit(x_train_tfidf,y_train)

y_pred = model.predict(x_test_tfidf)

accuracy_value = accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy_value*100)
print("\nClassification report:\n")
print(classification_report(y_test,y_pred))

joblib.dump(vectorizer, "Vectorizer.pkl")
joblib.dump(model, "BCC_model.pkl")

input_pdf_path = 'cleaned_output.pdf'  # Replace with your actual PDF path
output_folder_path = 'classified_out.pdf'  # Ensure this folder exists or create it
process_and_classify_pdf(input_pdf_path, output_folder_path)