from flask import Flask, request, jsonify
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#load NPL model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def preprocess_text(text):
    text = text.lower()                         #to lower case
    text = re.sub(r'[^a-zA-Z0-9 ]','',text)     #Remove Special Characters
    doc = nlp(text)                             #text is passed through an NLP pipeline
    # lemma creats base fom of tokens. Stopwords are removed.
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    print("Tokens : ",tokens)
    return "".join(tokens)                      #Joins the tokens with Spaces.

@app.route("/match", methods=["POST"])          # routing for resume upload URL.
def match_resume():
    data = request.json                                             # data received from API
    resume_text = preprocess_text(data.get("resume"))               # preprocessing resume text
    job_desc_text = preprocess_text(data.get("job_description"))    # preprocessing Job description text

    # creates tfidVectorizer used to convert text into numerical values based on word importance.
    # Words that appear frequently in a document but rarely in others are given higher importance.
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text,job_desc_text])
    similarity = cosine_similarity(vectors[0],vectors[1])[0][0]
    return jsonify({"match_score": similarity})