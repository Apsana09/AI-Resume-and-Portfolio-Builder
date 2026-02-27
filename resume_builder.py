import streamlit as st
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="AI Resume Studio", layout="wide")

# ----------------- CUSTOM STYLING -----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
}

[data-testid="stHeader"] {
    background: transparent;
}


            
h1, h2, h3, h4 {
    color: white;
}

.stTextInput>div>div>input,
.stTextArea textarea {
    background-color: white;
    color: black;
    border-radius: 10px;
}

div.stButton > button {
    background-color: #111827;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
            
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(10px);
border-radius: 20px;
padding: 20px;
                       
</style>
""", unsafe_allow_html=True)

st.title("✨ AI Resume & Portfolio Studio")

# ----------------- GEMINI CLIENT -----------------
client = genai.Client(api_key="AIzaSyAWRhQS4E3rNwMgHbBPwlU4MapOVKb0Y5s")

# ----------------- INPUT SECTION -----------------
st.header("📝 Enter your Details")
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
job_role = st.text_input("Target Job Role")
skills = st.text_area("Skills (comma separated)")
projects = st.text_area("Projects (brief description)")
experience = st.text_area("Experience")
education = st.text_area("Education")

template = st.selectbox("Choose Resume Style",
                        ["Modern", "Corporate", "Minimal"])

if template == "Modern":
    tone = "Modern and dynamic tone."
elif template == "Corporate":
    tone = "Formal corporate tone."
else:
    tone = "Clean and minimal tone."

st.divider()

# ----------------- GENERATE RESUME -----------------
if st.button("🚀 Generate Resume"):

    prompt = f"""
    Generate a professional ATS-friendly resume STRICTLY using only the details provided.

    Do NOT add fake achievements.
    Do NOT add extra experience.
    Only enhance wording professionally.

    DETAILS:
    Name: {name}
    Email: {email}
    Phone: {phone}
    Skills: {skills}
    Projects: {projects}
    Experience: {experience}
    Education: {education}
    Target Role: {job_role}

    Format clearly with headings:
    - PROFESSIONAL SUMMARY
    - SKILLS
    - PROJECTS
    - EXPERIENCE
    - EDUCATION

    Keep it realistic and concise.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    resume_text = response.text

    # ---------------- DISPLAY WITH COLORS ----------------
    st.markdown("### 🎨 Generated Resume")
    st.markdown(
        f"""
        <div style="background-color:white;padding:20px;border-radius:15px;color:black;">
        {resume_text.replace('\n','<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ----------------- PDF GENERATION -----------------
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontSize=11,
        leading=14
    )

    for line in resume_text.split("\n"):
        elements.append(Paragraph(line, custom_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    buffer.seek(0)

    st.download_button(
        "⬇ Download Resume PDF",
        buffer,
        file_name="AI_Resume.pdf",
        mime="application/pdf"
    )

# all input fields here

st.markdown("</div>", unsafe_allow_html=True)

if st.button("✨ Generate Professional Summary"):
    summary_prompt = f"""
    Write a powerful 4-5 line professional summary for:
    Name: {name}
    Skills: {skills}
    Experience: {experience}
    Target Role: {job_role}

    Make it impactful and ATS-friendly.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=summary_prompt
    )

    st.markdown("### 💼 Career Summary")
    st.success(response.text)

if skills:
    st.markdown("### 📊 Skill Strength Overview")

    skill_list = [s.strip() for s in skills.split(",")]

    for skill in skill_list:
        st.progress(0.8)
        st.write(f"🔹 {skill}")

if st.button("📈 Evaluate Resume Strength"):

    score_prompt = f"""
    Evaluate this profile:
    Skills: {skills}
    Projects: {projects}
    Experience: {experience}
    Education: {education}

    Give:
    - Overall Resume Score (out of 100)
    - 3 Strengths
    - 3 Areas of Improvement
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=score_prompt
    )

    st.markdown("### 🧠 AI Resume Analysis")
    st.info(response.text)

if st.button("🌐 Generate Portfolio Bio"):

    bio_prompt = f"""
    Write a modern personal portfolio bio for:
    Name: {name}
    Skills: {skills}
    Projects: {projects}
    Keep it professional but engaging.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=bio_prompt
    )

    st.markdown("### 🌟 Portfolio Bio")
    st.success(response.text)


def keyword_match_score(skills, jd_text):
    skill_list = [s.strip().lower() for s in skills.split(",")]
    jd_text = jd_text.lower()

    matches = sum(1 for skill in skill_list if skill in jd_text)

    if len(skill_list) == 0:
        return 0

    return round((matches / len(skill_list)) * 100, 2)

# 👇 Put headings OUTSIDE spinner
st.markdown("""
<div style="display:flex; justify-content:space-around; margin-top:50px;">
    <h3>🎯 Target Role</h3>
    <h3>🛠 Skills</h3>
    <h3>🚀 Projects</h3>
</div>
""", unsafe_allow_html=True)
# ----------------- FOOTER -----------------
st.markdown("""
<hr>
<center><b>Built with ❤️ using AI | 6th Semester AI Project</b></center>
""", unsafe_allow_html=True)