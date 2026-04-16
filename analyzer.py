
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
        



TECH_MASTER = {
    "python", "java", "javascript", "react", "node.js", "aws",
    "docker", "kubernetes", "sql", "mysql", "postgresql",
    "mongodb", "git", "html", "css", "typescript",
    "flask", "django", "streamlit", "rest api"
}

def load_skills(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return {line.strip().lower() for line in file if line.strip()}

TECH_MASTER = load_skills("tech_skills.txt")
SOFT_MASTER = load_skills("soft_skills.txt")


def extract_skills_from_jb(jd_text):
    jd_doc = nlp(jd_text)
    jd_tokens = set(token.lemma_.lower() for token in jd_doc if token.is_alpha)
    jd_tech_skills = jd_tokens.intersection(TECH_MASTER)
    jd_soft_skills = jd_tokens.intersection(SOFT_MASTER)
    return jd_tech_skills, jd_soft_skills



def check_resume(resume_text, jd_description):
    resume = resume_text.lower()
    jd_text,jd_soft = extract_skills_from_jb(jd_description)
    
    matched_tech = [s  for s in jd_text if s in resume]
    missing_tech = [s for s in jd_text if s not in resume]
    
    matched_soft = [s for s in jd_soft if s in resume]
    missing_soft = [s for s in jd_soft if s not in resume]
    
    return matched_tech, missing_tech, matched_soft, missing_soft
 


    
        




