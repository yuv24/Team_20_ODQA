!pip install nltk PyMuPDF
import fitz
import nltk
import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def preprocess_text(text):

    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'[^\w\s.,:;!?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    normalized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in normalized_tokens if token not in stop_words]
    preprocessed_text = ' '.join(filtered_tokens)
    preprocessed_text = re.sub(r'\s+([,.!?])', r'\1', preprocessed_text)
    preprocessed_text = re.sub(r'([,.!?])\1+', r'\1', preprocessed_text)
    return preprocessed_text

pdf_directory = 'ncert_pdfs'

for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        subject_name = os.path.splitext(filename)[0]
        pdf_path = os.path.join(pdf_directory, filename)
        extracted_text = extract_text_from_pdf(pdf_path)
        preprocessed_text = preprocess_text(extracted_text)

        output_file_path = os.path.join(pdf_directory, f'preprocessed_{subject_name}.txt')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(preprocessed_text)
        print(f'Processed and saved: {output_file_path}')