import streamlit as st
from analyzer import preprocesstext, calculate_similarity, find_missing_keywords, find_filtered_keywords, extract_text

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

        # find the missing keywords in the resume
        missing_keywords = find_missing_keywords(resume_clean, jd_clean)
        
        #filter the missing keywords based on categories (e.g., skills, experience, education)
        
        filltered_keywords = find_filtered_keywords(missing_keywords)
        tech_skills, soft_skills, other = filltered_keywords
        
        if(tech_skills):
            st.subheader("Missing Technical Skills:")
            for skill in tech_skills:
                st.write(f"- {skill}")

        if(soft_skills):
            st.subheader("Missing Soft Skills:")
            for skill in soft_skills:
                st.write(f"- {skill}")
        
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
                
