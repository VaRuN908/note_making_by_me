import os
import io
from flask import Flask, request, render_template
import spacy
from spacy import displacy
import fitz  # PyMuPDF for PDF
from docx import Document  # python-docx for DOCX
import pandas as pd  # pandas for CSV

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

def extract_text(file):
    filename = file.filename.lower()
    file_bytes = file.read()
    
    # Handle PDF
    if filename.endswith('.pdf'):
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    
    # Handle DOCX
    elif filename.endswith('.docx'):
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([para.text for para in doc.paragraphs])
    
    # Handle CSV
    elif filename.endswith('.csv'):
        # Using handle as file-like object for pandas
        df = pd.read_csv(io.BytesIO(file_bytes))
        # Convert all content to string and join
        return df.to_string(index=False)
    
    # Default to text
    else:
        try:
            return file_bytes.decode('utf-8', errors='ignore')
        except:
            return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entity', methods=['POST', 'GET'])
def entity():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            readable_file = extract_text(file)
            if readable_file.strip():
                docs = nlp(readable_file)
                
                if docs.ents:
                    html = displacy.render(docs, style='ent', jupyter=False)
                else:
                    html = "<div class='alert alert-warning mt-3'>No named entities to visualize were found in the uploaded file.</div>"
                    
                return render_template('index.html', html=html, text=readable_file)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)