from flask import Flask, request, jsonify
import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP model
nlp = spacy.load("en_core_web_sm")

app = Flask("__name__")

# Common technical keywords (customizable)
TECH_KEYWORDS = {
    "python", "ai", "ml", "tensorflow", "pytorch", "nlp", "data", "science",
    "machine", "learning", "deep", "neural", "network", "developer", "engineer",
    "software", "fullstack", "backend", "frontend", "database", "cloud", "aws"
}

# Synonyms mapping (expandable)
SYNONYMS = {
    "engineer": "developer",
    "expertise": "experience",
    "deep learning": "machine learning",
    "neural network": "machine learning",
    "ml": "machine learning",
    "ai": "artificial intelligence"
}

def preprocess_text(text):
    """Preprocess text: normalize, replace synonyms, and retain key terms."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)  # Keep spaces instead of removing them
    text = text.replace("aiml", "ai ml")  # Fix "aiml" to "ai ml"

    doc = nlp(text)

    tokens = []
    for token in doc:
        lemma = SYNONYMS.get(token.lemma_, token.lemma_)  # Replace with synonym if available
        if lemma in TECH_KEYWORDS or not token.is_stop:  # Keep important words
            tokens.append(lemma)

    print("Processed Text:", " ".join(tokens))
    return " ".join(tokens)

@app.route("/match", methods=["POST"])
def match_resume():
    """API endpoint to compute resume-job description similarity."""
    data = request.json

    resume_text = preprocess_text(data.get("resume", ""))
    job_desc_text = preprocess_text(data.get("job_description", ""))

    if not resume_text or not job_desc_text:
        return jsonify({"match_score": 0.0, "error": "Preprocessed text is empty"})

    # TF-IDF vectorization with n-grams for better phrase matching
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=5000, sublinear_tf=True, use_idf=True)
    vectors = vectorizer.fit_transform([resume_text, job_desc_text])

    # Compute bi-directional similarity
    similarity_1 = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    similarity_2 = cosine_similarity(vectors[1:2], vectors[0:1])[0][0]
    final_similarity = (similarity_1 + similarity_2) / 2  # Average for better accuracy

    print("\n=== Cosine Similarity Score ===")
    print(f"Match Score: {final_similarity}")

    return jsonify({"match_score": final_similarity})

if __name__ == "__main__":
    app.run(debug=True)
