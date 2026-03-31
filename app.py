from flask import Flask,request,render_template
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/entity', methods=['POST', 'GET'])
def entity():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            readable_file = file.read().decode('utf-8', errors='ignore')
            docs = nlp(readable_file)
            
            if docs.ents:
                html = displacy.render(docs, style='ent', jupyter=False)
            else:
                html = "<div class='alert alert-warning mt-3'>No named entities to visualize were found in the uploaded text.</div>"
                
            return render_template('index.html', html=html, text=readable_file)
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)