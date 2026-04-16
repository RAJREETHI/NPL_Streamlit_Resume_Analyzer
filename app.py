import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from analyzer import preprocesstext, calculate_similarity, extract_text, check_resume

import spacy
import subprocess

try:
    nlp = spacy.load("en_core_web_sm")
except:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

st.title("🚀 AI Resume Analyser")
st.markdown("Analyze how well your resume matches a job description using AI.")
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx", "txt"])

with col2:
    job_description_file = st.file_uploader("📑 Upload Job Description", type=["pdf", "docx", "txt"])
    


if resume_file:
    st.success("Resume uploaded successfully! ✅")

if job_description_file:
    st.success("Job description uploaded successfully! ✅")

if resume_file and job_description_file:
    # function to convert the file type to text
 if st.button("🔍 Analyze Match"):
    resume_text = extract_text(resume_file)
    jd_text = extract_text(job_description_file)
    
    if resume_text is None or jd_text is None:
        st.error("Unsupported file type. Please upload a .txt, .pdf, or .docx file.")
    else:
        resume_clean = preprocesstext(resume_text)
        jd_clean = preprocesstext(jd_text)
        
        matched_tech, missing_tech, matched_soft, missing_soft = check_resume(resume_clean, jd_clean)
        
        score = calculate_similarity(resume_clean, jd_clean)
        st.subheader("📊 Match Score")
        st.progress(score / 100)
        st.metric(label="Score", value=f"{score}%")
        
        if score > 80:
           st.success("Excellent match! 🎯")
        elif score > 60:
           st.warning("Good match, but can improve ⚡")
        else:
           st.error("Low match — needs improvement ❗")
            

        
        if(missing_tech):
            st.subheader("Missing Technical Skills:")
            for skill in missing_tech:
                st.write(f"- {skill.upper()}")

        if(missing_soft):
            st.subheader("Missing Soft Skills:")
            for skill in missing_soft:
                st.write(f"- {skill.upper()}")
        
            if resume_file and job_description_file and score is not None:
             tab1, tab2, tab3 = st.tabs(["📊 Results", "📄 Resume", "📑 JD"])

             with tab1:
                st.metric("Score", f"{score}%")

             with tab2:
                st.write(resume_text)

             with tab3:
                st.write(jd_text)    
                
                
st.markdown("""
<style>
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)                    
                
