
#spaCY (for text processing)
#Scikit-learn (for machine learning)
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# file handling
import PyPDF2
from docx import Document

def extract_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")

    elif file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_type == "docx":
        doc = Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return None

nlp = spacy.load('en_core_web_sm')

def preprocesstext(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and  token.is_alpha]
    return ' '.join(tokens)

def calculate_similarity(resume, jd):
    texts = [resume, jd]
    cv = CountVectorizer()
    matrix = cv.fit_transform(texts)
    similarity = cosine_similarity(matrix)[0][1]
    return round(similarity*100,2)

def find_missing_keywords(resume, jd):
    resume_keywords = set(resume.split())
    jd_clean_keywords = set(jd.split())
    missing_keywords = jd_clean_keywords - resume_keywords
    # if missing_keywords:
    #     for keyword in sorted(missing_keywords):
    #         st.write(f"- {keyword}")
    # else:
    #     st.write("No missing keywords found. Your resume is well-aligned with the job description!")
     
    return missing_keywords
        
# Example grouping logic (basic)
def find_filtered_keywords(missing_keywords):
    tech_skills = []
    soft_skills = []
    other = []
    t_skills = ["python", "aws", "react", "sql", "docker","sqlalchemy"] 
    s_skills = ["communication", "leadership", "teamwork"]
    for word in missing_keywords:
        if any(t_skill in word.lower() for t_skill in t_skills):
            tech_skills.append(word)
        elif any(s_skill in word.lower() for s_skill in s_skills):
            soft_skills.append(word)
        else:
            other.append(word)
    return tech_skills, soft_skills, other

    
        




