import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path

# Title for the website "💼 Smart Career Companion.AI"
st.set_page_config(
    page_title="CAREERCRAFT JOB.AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# Smart Job Assistant\nPowered by Gen AI 🚀"})
# Packages 
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai
from groq import Groq
import docx2txt
from datetime import datetime
import re
import logging
import random
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (local development)
load_dotenv()

# Helper to check if secrets.toml exists
def secrets_file_exists():
    # Default Streamlit secrets paths
    user_path = Path.home() / ".streamlit" / "secrets.toml"
    cwd_path = Path.cwd() / ".streamlit" / "secrets.toml"
    return user_path.exists() or cwd_path.exists()

# Get API keys
# if secrets_file_exists():
#     gemini_api_key = st.secrets.get('Google_Gemini_ai_key', None)
#     groq_api_key = st.secrets.get('Groq_api_key', None)
# else:
#     gemini_api_key = os.getenv('Google_Gemini_ai_key')
#     groq_api_key = os.getenv('Groq_api_key')

gemini_api_key = os.getenv('Google_Gemini_ai_key')  # (ya jo bhi aap use karte hain)
groq_api_key = "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"
# st.write(f"API Key: {groq_api_key}")  # Debug line (REMOVED for security)

# DEBUG: Show loaded keys in terminal (not in UI for security)
print("Gemini API Key Loaded:", bool(gemini_api_key))
print("Groq API Key Loaded:", bool(groq_api_key))
print("Groq API Key Value:", repr(groq_api_key))  # Add this line

# Configure Gemini AI
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    # st.success('✅ Google Gemini AI configured successfully!')  # HIDDEN: No success message in UI
else:
    st.error("⚠️ Google Gemini API key not found. Please check your configuration.")

# Configure Groq AI
try:
    if not groq_api_key:
        st.warning("⚠️ Groq API key not found. Some features may be limited.")
        groq_client = None
    else:
        # DEBUG: Try to initialize Groq client and print result
        try:
            groq_client = Groq(api_key=groq_api_key)
            # st.success('✅ Groq AI configured successfully!')  # HIDDEN: No success message in UI
            print("Groq client initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing Groq client: {str(e)}")
            st.error(f"⚠️ Error initializing Groq client: {str(e)}")
            groq_client = None
except Exception as e:
    logger.error(f"Error initializing Groq client: {str(e)}")
    st.warning("⚠️ Error initializing Groq client. Some features may be limited.")
    groq_client = None

# --- Interactive Resume Editor Feature (ALWAYS AT TOP) ---
def extract_resume_fields_from_pdf(pdf_path):
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        import re
        fields = {}
        lines = text.splitlines()
        fields["Name"] = lines[0].strip() if lines else ""
        email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
        fields["Email"] = email_match.group(0) if email_match else ""
        phone_match = re.search(r"(\+?\d[\d\s-]{8,})", text)
        fields["Phone"] = phone_match.group(0) if phone_match else ""
        summary_match = re.search(r"Summary[:\-\s]*([\s\S]*?)(?=\n\w+:|\nSkills|\nExperience|\nEducation|\n$)", text, re.IGNORECASE)
        fields["Summary"] = summary_match.group(1).strip() if summary_match else ""
        skills_match = re.search(r"Skills[:\-\s]*([\s\S]*?)(?=\n\w+:|\nExperience|\nEducation|\n$)", text, re.IGNORECASE)
        fields["Skills"] = skills_match.group(1).strip() if skills_match else ""
        exp_match = re.search(r"Experience[:\-\s]*([\s\S]*?)(?=\n\w+:|\nEducation|\n$)", text, re.IGNORECASE)
        fields["Experience"] = exp_match.group(1).strip() if exp_match else ""
        edu_match = re.search(r"Education[:\-\s]*([\s\S]*?)(?=\n\w+:|\nCertifications|\nAchievements|\n$)", text, re.IGNORECASE)
        fields["Education"] = edu_match.group(1).strip() if edu_match else ""
        cert_match = re.search(r"Certifications[:\-\s]*([\s\S]*?)(?=\n\w+:|\nAchievements|\n$)", text, re.IGNORECASE)
        fields["Certifications"] = cert_match.group(1).strip() if cert_match else ""
        ach_match = re.search(r"Achievements[:\-\s]*([\s\S]*?)(?=\n\w+:|\n$)", text, re.IGNORECASE)
        fields["Achievements"] = ach_match.group(1).strip() if ach_match else ""
        return fields
    except Exception as e:
        return {"Name": "", "Email": "", "Phone": "", "Summary": "", "Skills": "", "Experience": "", "Education": "", "Certifications": "", "Achievements": ""}

def interactive_resume_editor_tab():
    import streamlit as st
    import os
    st.markdown('''
        <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 class="title-glow">📝 Interactive Resume Editor</h1>
            <p style="color: #43e97b;">Edit your resume in real time, see live preview, and download instantly!</p>
        </div>
    ''', unsafe_allow_html=True)
    st.success("Interactive Resume Editor tab is OPEN! (If you see this, the tab is working)")
    print("DEBUG: Interactive Resume Editor tab opened!")
    resume_path = os.path.join(os.getcwd(), "My Resume.pdf")
    fields = extract_resume_fields_from_pdf(resume_path)
    with st.form("resume_edit_form"):
        name = st.text_input("Full Name", value=fields.get("Name", ""))
        email = st.text_input("Email", value=fields.get("Email", ""))
        phone = st.text_input("Phone", value=fields.get("Phone", ""))
        summary = st.text_area("Professional Summary", value=fields.get("Summary", ""))
        skills = st.text_area("Skills", value=fields.get("Skills", ""))
        experience = st.text_area("Experience", value=fields.get("Experience", ""))
        education = st.text_area("Education", value=fields.get("Education", ""))
        certifications = st.text_area("Certifications", value=fields.get("Certifications", ""))
        achievements = st.text_area("Achievements", value=fields.get("Achievements", ""))
        submitted = st.form_submit_button("Update Preview")
    st.markdown("### 👀 Live Resume Preview")
    preview_html = f"""
    <div class='glass-card' style='padding:1.5rem;'>
    <h2 style='color:#ff6f61;'>{name}</h2>
    <b>Email:</b> {email} &nbsp; <b>Phone:</b> {phone}<br><br>
    <b>Summary:</b><br>{summary}<br><br>
    <b>Skills:</b><br>{skills}<br><br>
    <b>Experience:</b><br>{experience}<br><br>
    <b>Education:</b><br>{education}<br><br>
    <b>Certifications:</b><br>{certifications}<br><br>
    <b>Achievements:</b><br>{achievements}
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)
    resume_text = f"""{name}\nEmail: {email}\nPhone: {phone}\n\nSummary:\n{summary}\n\nSkills:\n{skills}\n\nExperience:\n{experience}\n\nEducation:\n{education}\n\nCertifications:\n{certifications}\n\nAchievements:\n{achievements}\n"""
    st.download_button("💾 Download Resume (TXT)", resume_text, file_name="custom_resume.txt")
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in resume_text.splitlines():
            pdf.cell(0, 10, line, ln=1)
        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button("💾 Download Resume (PDF)", pdf_output, file_name="custom_resume.pdf")
    except Exception:
        st.info("Install 'fpdf' for PDF download support.")

class ATSAnalyzer:
    # Language prompts dictionary
    LANGUAGE_PROMPTS = {
        "English": {
            "resume_analysis": """
Analyze the resume and provide:
1. Match Score (%)
2. Key Strengths
3. Missing Skills
4. Improvement Suggestions
            """,
            "labels": {
                "upload": "Upload your resume (PDF or DOC/DOCX format)",
                "job_desc": "Job Description",
                "analyze": "Analyze Resume",
                "results": "Analysis Results"
            }
        },
        "हिंदी": {
            "resume_analysis": """
रिज्यूमे का विश्लेषण करें और प्रदान करें:
1. मैच स्कोर (%)
2. प्रमुख शक्तियां
3. कमी वाले कौशल
4. सुधार के सुझाव
            """,
            "labels": {
                "upload": "अपना रिज्यूमे अपलोड करें (PDF या DOC/DOCX प्रारूप)",
                "job_desc": "नौकरी का विवरण",
                "analyze": "रिज्यूमे का विश्लेषण करें",
                "results": "विश्लेषण परिणाम"
            }},
        "తెలుగు": {
            "resume_analysis": """
రెస్యూమ్ విశ్లేషణ చేసి ఈ క్రింది వాటిని అందించండి:
1. మ్యాచ్ స్కోర్ (%)
2. ముఖ్య బలాలు
3. కొరవడిన నైపుణ్యాలు
4. మెరుగుదల సూచనలు
            """,
            "labels": {
                "upload": "మీ రెస్యూమ్‌ని అప్‌లోడ్ చేయండి (PDF లేదా DOC/DOCX ఫార్మాట్)",
                "job_desc": "ఉద్యోగ వివరణ",
                "analyze": "రెస్యూమ్ విశ్లేషించండి",
                "results": "విశ్లేషణ ఫలితాలు"
            }}}

    # Analysis types with their prompts
    ANALYSIS_TYPES = {
        "Complete Analysis": """Analyze my resume against the provided job description(s) and provide a comprehensive evaluation, including:
1.Overall Match Score (0 to 100): Calculate the candidate's overall suitability (%). Explain the weighting of Key Skills, Experience, and Education.

2.Key Skills Match:
Matching: List proficient skills.
Potential: List skills needing assessment.
Missing: List crucial missing skills.

3.Experience Alignment:
Relevant: Detail correlating experience, quantifying achievements.
Transferable: Identify applicable skills from other roles.
Gaps: Note experience gaps.

4.Education Fit:
Required: State minimum qualifications.
Candidate's: List degrees, certifications, coursework.
Gaps: Identify education discrepancies.
Improvement Suggestions: Offer constructive feedback for strengthening their profile.
        """,
         "ATS Optimization": """
I need you to act as an expert resume writer and optimization specialist. Your ultimate goal is to create a powerful and highly effective resume for me that excels in all aspects: ATS compatibility, recruiter appeal, and alignment with industry best practices.

1.ATS Compatibility Analysis:Thoroughly review my resume for any elements that might hinder its performance in ATS scans.  Identify specific areas for improvement, including:Formatting issues (e.g., use of tables, images, special characters, unusual fonts)
File format (recommend the most ATS-friendly format)
Keyword optimization (lack of relevant keywords, keyword stuffing)
Section headings and organization (ensure logical structure and standard headings)
Date formats and other data inconsistencies

2.Content Enhancement for Recruiter Appeal:  Suggest specific changes to better highlight my technical skills, projects, and achievements.  Focus on making these elements stand out to recruiters:
Quantifiable achievements:Help me rephrase accomplishments to showcase quantifiable results (e.g., "Increased sales by 15%" instead of "Increased sales").
Project descriptions: Advise on how to write concise and compelling project descriptions that emphasize my contributions and the project's impact.
Technical skills: Ensure my technical skills are prominently displayed and categorized effectively. Suggest ways to showcase proficiency levels (e.g., beginner, intermediate, expert).
Impactful language: Help me use action verbs and strong language to make my resume more dynamic and engaging.

3.Industry Alignment and Tailoring: Provide recommendations on how to tailor my resume language and structure to align with common industry standards and specific job descriptions.
This includes Keyword matching:Explain how to identify and incorporate relevant keywords from job descriptions.
Industry-specific terminology: Suggest appropriate terminology and jargon to use.

4.Resume length and format: Advise on the ideal length and format for my industry and experience level.
        """,
        "Skills Gap Analysis": """
        Provide a concise skills analysis for the candidate, focusing on the following areas:
1.Matching Skills: List the candidate's skills that directly align with the job requirements, quantifying their proficiency where possible.
2.Missing Critical Skills: List the essential skills required for the role that the candidate lacks, prioritizing them based on their importance to job performance.
3.Recommended Skills to Add: List skills that would significantly enhance the candidate's suitability for the role or their future growth within the company, explaining the rationale behind each recommendation.
4.Skill Level Assessment: Provide a qualitative assessment of the candidate's skill level for each matching skill using terms like Beginner, Intermediate, Proficient, and Expert.
        """,
        "Quick Summary": """
Provide a brief overview:
1.Match: Overall suitability (%). Weighting of criteria (e.g., skills, experience, education).
2.Strengths: Top 3, with examples.
3.Gaps: Top 3, prioritized.
4.Next Steps: 2-3 recommendations.
        """}

    # AI models
    AI_MODELS = {"Google Gemini": "🤖 Google Gemini (High accurate and reliable)","Groq": "🤖 Groq (Fast but moderately accurate)"}

    # Cold mail 
    COLD_MAIL_TYPES = {
        "📑 Professional and Straightforward": {
            "description": "A formal and direct approach, ideal for traditional industries and corporate settings",
            "template": """
Subject: Seeking Internship Opportunity to Learn and Contribute

Dear [Recipient's Name],

I hope you're doing well. My name is [Your Name], and I am currently a [Your Year] student pursuing [Your Degree] at [Your College/University Name].

I am writing to express my interest in an internship opportunity at [Company Name]. I have been following your company's work in [specific field/area], and I am truly inspired by your innovative contributions to the industry.

My academic background and hands-on experience in [specific skills/tools] have prepared me to contribute meaningfully to your team. I am eager to learn from industry experts like you and enhance my skills further.

Could we connect to discuss any available internship opportunities? I have attached my resume for your review and would be happy to provide additional information if needed. Thank you for considering my application. I look forward to the possibility of contributing to your team.

Warm regards,
[Your Full Name]
[Your Phone Number]
[Your Email Address]
[LinkedIn Profile link or Portfolio]
            """
        },
        "🤝 Friendly Yet Professional": {
            "description": "A balanced approach combining warmth with professionalism, suitable for modern companies and startups",
            "template": """
Subject: Excited to Learn and Contribute - Internship Inquiry

Hi [Recipient's Name],

I hope you're having a great day! I'm [Your Name], currently pursuing [Your Degree] at [Your College/University Name], and I'm reaching out to explore internship opportunities with [Company Name].

I've always admired your company's commitment to [specific value or field]. As someone passionate about [specific area], I believe this could be an incredible place for me to learn and grow.

I've gained practical knowledge in [specific skills or projects] and I'm eager to contribute to your team while gaining real-world experience in the industry/role.

Would it be possible to discuss how I can support your team? I've attached my resume for your reference and would be delighted to provide any further details. Looking forward to hearing from you!

Best regards,
[Your Full Name]
[Your Phone Number]
[Your Email Address]
[LinkedIn Profile Link or Portfolio]
            """
        },
        "🌟 Enthusiastic and Curious": {
            "description": "An energetic approach emphasizing eagerness to learn and contribute, great for innovation-focused companies",
            "template": """
Subject: Internship Inquiry: Eager to Learn and Make an Impact

Dear [Recipient's Name],

I hope this email finds you well. My name is [Your Name], and I am a [Year of Study] student specializing in [Your Field of Study] at [Your College/University Name].

I am writing to express my interest in an internship opportunity at [Company Name]. Your organization's work in [specific domain] has always inspired me, particularly [mention a specific project, value, or achievement of the company].

With foundational experience in [your skills/experience], I'm keen to contribute to your team while learning from the expertise of your professionals. I'm confident that this internship will give me an opportunity to develop my skills and create value for your organization.

I would be thrilled to connect and discuss how I can contribute to your team. I've attached my resume for your consideration. Thank you for your time, and I look forward to hearing from you.

Best regards,
[Your Full Name]
[Your Phone Number]
[Your Email Address]
[LinkedIn Profile Link or Portfolio]
            """}}

    @staticmethod
    def get_prompts(language="English"):
        """Get language-specific prompts"""
        prompts = {
            "English": {
                "system_msg": """You are a professional resume analyzer. Your task is to analyze resumes in English.\nAlways structure your response as follows:\n1. Match Score (%)\n2. Key Strengths\n3. Missing Skills\n4. Improvement Suggestions""",
                "user_msg": """Please analyze this resume against the job description in English.\nEnsure you follow the exact format mentioned above.""",
                "result_prefix": "Analysis Results:\n\n"
            },
            "हिंदी": {
                "system_msg": """आप एक पेशेवर रिज्यूमे विश्लेषक हैं। आपका काम रिज्यूमे का विश्लेषण हिंदी में करना है।\nकृपया अपना जवाब इस प्रारूप में दें:\n1. मैच स्कोर (%)\n2. मुख्य ताकत\n3. कमी वाले कौशल\n4. सुधार के सुझाव""",
                "user_msg": """कृपया इस रिज्यूमे का विश्लेषण नौकरी के विवरण के अनुसार हिंदी में करें।\nकृपया ऊपर दिए गए प्रारूप का पालन करें।""",
                "result_prefix": "विश्लेषण परिणाम:\n\n"
            },
            "తెలుగు": {
                "system_msg": """మీరు ఒక వృత్తిపరమైన రెస్యూమ్ విశ్లేషకులు. మీ పని రెస్యూమ్‌ని తెలుగులో విశ్లేషించడం.\nదయచేసి మీ సమాధానాన్ని ఈ ఫార్మాట్‌లో ఇవ్వండి:\n1. మ్యాచ్ స్కోర్ (%)\n2. ముఖ్య బలాలు\n3. కొరవడిన నైపుణ్యాలు\n4. మెరుగుదల సూచనలు""",
                "user_msg": """దయచేసి ఈ రెస్యూమ్‌ని ఉద్యోగ వివరణతో పోల్చి తెలుగులో విశ్లేషించండి.\nపైన పేర్కొన్న ఫార్మాట్‌ని ఖచ్చితంగా పాటించండి.""",
                "result_prefix": "విశ్లేషణ ఫలితాలు:\n\n"
            }
        }
        return prompts.get(language, prompts["English"])

    @staticmethod
    def get_error_message(language):
        """Get language-specific error messages"""
        error_messages = {
            "English": "Error in analysis. Please try again or contact support.",
            "हिंदी": "विश्लेषण में त्रुटि हुई। कृपया पुनः प्रयास करें या सहायता से संपर्क करें।",
            "తెలుగు": "విశ్లేషణలో లోపం. దయచేసి మళ్లీ ప్రయత్నించండి లేదా సహాయం కోసం సంప్రదించండి."}
        return error_messages.get(language, error_messages["English"])

    @staticmethod
    def format_groq_messages(selected_lang, input_prompt, job_description, pdf_text, language):
        """Format messages for Groq API"""
        return [{"role": "system","content": selected_lang["system_msg"]},{"role": "user","content": f"""{selected_lang["user_msg"]}

Analysis Requirements:
{input_prompt}

Job Description:
{job_description}

Resume Content:
{pdf_text}

Remember to:
1. Keep the analysis in {language}
2. Follow the exact format specified
3. Provide clear, actionable feedback
4. Include a numerical match score"""}]

    @staticmethod
    def get_ai_response(model_choice, input_prompt, pdf_text, job_description, language="English"):
        """Get AI response from selected model"""
        try:
            selected_lang = ATSAnalyzer.get_prompts(language)
            
            if model_choice == "Google Gemini":
                return ATSAnalyzer.get_gemini_response(input_prompt, pdf_text, job_description, language)
            
            # For Groq model
            if groq_client is None:
                st.error("⚠️ Groq AI is not available. Please use Google Gemini instead.")
                return ATSAnalyzer.get_gemini_response(input_prompt, pdf_text, job_description, language)
                
            messages = ATSAnalyzer.format_groq_messages(selected_lang, input_prompt, job_description, pdf_text, language)

            # Using mistral model with optimized parameters
            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=messages,
                    model="mistral-saba-24b",
                    temperature=0.5,
                    max_tokens=4000,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0)
                response = chat_completion.choices[0].message.content
                if not response or len(response.strip()) < 10:
                    raise Exception("Invalid or empty response received")
                return selected_lang["result_prefix"] + response
            except Exception as e:
                logger.error(f"Groq API Error: {str(e)}")
                st.error(f"Groq API Error: {str(e)}")
                return ATSAnalyzer.get_error_message(language)
            
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            st.error(f"API Error: {str(e)}")
            return ATSAnalyzer.get_error_message(language)

    @staticmethod
    def get_gemini_response(input_prompt, pdf_text, job_description, language="English"):
        try:
            if not pdf_text or not job_description:
                logger.error("Empty resume text or job description")
                st.error("⚠️ Resume text or job description is empty. Please check your inputs.")
                return None

            logger.debug("Attempting to initialize Gemini model with models/gemini-1.5-flash-latest")
            try:
                model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                logger.debug("Successfully initialized models/gemini-1.5-flash-latest model")
            except Exception as e:
                logger.error(f"Failed to initialize models/gemini-1.5-flash-latest: {str(e)}")
                st.error("⚠️ Failed to initialize Gemini free model.")
                return None

            try:
                full_prompt = f"""
Task: {input_prompt}

Language: {language}

Resume Content:
{pdf_text}

Job Description:
{job_description}

Please provide a detailed analysis based on the above information.
"""
                logger.debug(f"Sending request to Gemini API with prompt length: {len(full_prompt)}")
                response = model.generate_content(full_prompt)
                logger.debug("Successfully received response from Gemini API")
                return response.text
            except Exception as e:
                logger.error(f"Error generating Gemini response: {str(e)}")
                st.error(f"Error generating response: {str(e)}")
                return None
        except Exception as outer_e:
            logger.error(f"Unexpected error in get_gemini_response: {str(outer_e)}")
            st.error(f"Unexpected error: {str(outer_e)}")
            return None

    @staticmethod
    def extract_text(uploaded_file):
        try:
            file_type = uploaded_file.name.split('.')[-1].lower()
            if file_type == 'pdf':
                pdf_reader = PdfReader(uploaded_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
            elif file_type in ['doc', 'docx']:
                return docx2txt.process(uploaded_file)
            else:
                st.error("Unsupported file format")
                return None
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            return None

    @staticmethod
    def extract_data_from_response(response):
        """Extract structured data from AI response"""
        try:
            # Extract match score
            match_pattern = r'Match Score:?\s*(\d+)%'
            match_result = re.search(match_pattern, response)
            match_score = float(match_result.group(1)) if match_result else 0

            return {'match_score': match_score,'raw_response': response}
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            return None

    @staticmethod
    def generate_cold_mail(model_choice, prompt, resume_text, job_description, personal_info):
        """Generate a cold mail using the selected AI model"""
        try:
            if model_choice == "Google Gemini":
                try:
                    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                except Exception as e:
                    logger.error(f"Failed to initialize models/gemini-1.5-flash-latest: {str(e)}")
                    st.error("⚠️ Failed to initialize Gemini free model.")
                    return None

                response = model.generate_content([prompt, resume_text, job_description])
                generated_content = response.text
            else:
                if groq_client is None:
                    st.error("⚠️ Groq AI is not available. Please use Google Gemini instead.")
                    try:
                        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                    except Exception as e:
                        logger.error(f"Failed to initialize models/gemini-1.5-flash-latest: {str(e)}")
                        st.error("⚠️ Failed to initialize Gemini free model.")
                        return None

                    response = model.generate_content([prompt, resume_text, job_description])
                    generated_content = response.text
                else: 
                    chat_completion = groq_client.chat.completions.create(
                        messages=[
                            {"role": "user","content": f"{prompt}\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}"}],
                        model="mistral-saba-24b",
                        temperature=0.5,)
                    generated_content = chat_completion.choices[0].message.content

            # Replace basic placeholders with personal information
            generated_content = generated_content.replace("[Your Name]", personal_info.get("name", "[Your Name]"))
            generated_content = generated_content.replace("[Your Email Address]", personal_info.get("email", "[Your Email]"))
            generated_content = generated_content.replace("[Your Phone Number]", personal_info.get("phone", "[Your Phone]"))
            generated_content = generated_content.replace("[Your College/University Name]", personal_info.get("university", "[Your University]"))
            generated_content = generated_content.replace("[LinkedIn Profile or Portfolio link]", personal_info.get("linkedin", "[Your LinkedIn]"))
            generated_content = generated_content.replace("[Your Degree]", personal_info.get("degree", "[Your Degree]"))

            return generated_content

        except Exception as e:
            logger.error(f"Error generating cold mail: {str(e)}")
            return None

def ai_resume_builder_tab():
    st.markdown('''
        <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 class="title-glow">🛠️ AI-Powered Resume Builder & Editor</h1>
            <p style="color: #06B6D4;">Build your resume with real-time AI feedback, ATS scoring, and keyword optimization.</p>
        </div>
    ''', unsafe_allow_html=True)

    st.info("**Tip:** Paste a job description to tailor your resume and maximize your ATS score!")

    # Optional: Target Job Description for tailoring
    job_desc = st.text_area("Target Job Description (Optional)", help="Paste the job description to optimize your resume for a specific role.")

    # Step-by-step resume builder with real-time feedback
    with st.form("resume_builder_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        summary = st.text_area("Professional Summary", help="Get AI suggestions for your summary.")
        skills = st.text_area("Skills (comma separated)", help="e.g., Python, Data Analysis, Communication")
        experience = st.text_area("Experience", help="Describe your work experience.")
        education = st.text_area("Education", help="List your degrees and certifications.")
        certifications = st.text_area("Certifications", help="List your certifications (optional).")
        achievements = st.text_area("Achievements", help="List your achievements (optional).")
        submitted = st.form_submit_button("Get AI Suggestions & ATS Score")

    if submitted:
        with st.spinner("Generating AI suggestions and ATS score..."):
            prompt = f"""
You are an expert resume builder and ATS optimizer. 
Given the following resume sections and the target job description, do the following:
1. Rewrite and enhance each section for clarity, impact, and ATS optimization.
2. Highlight missing keywords/skills from the job description.
3. Suggest action verbs and quantifiable achievements.
4. Format the resume for ATS compatibility.
5. Give an ATS Match Score (0-100%) and explain how to reach 100%.

Resume Sections:
Name: {name}
Email: {email}
Phone: {phone}
Summary: {summary}
Skills: {skills}
Experience: {experience}
Education: {education}
Certifications: {certifications}
Achievements: {achievements}

Job Description:
{job_desc if job_desc else "N/A"}
"""
            try:
                model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                response = model.generate_content(prompt)
                st.markdown("### ✨ AI Suggestions & Enhanced Resume")
                st.markdown(f"<div class='glass-card'><pre>{response.text}</pre></div>", unsafe_allow_html=True)

                # Remove ** ** from the text for download
                clean_text = response.text.replace("**", "")

                import re
                score_match = re.search(r'ATS Match Score\s*[:\-]?\s*(\d+)', response.text)
                if score_match:
                    score = int(score_match.group(1))
                    st.progress(score / 100, text=f"ATS Score: {score}%")
                    if score < 100:
                        st.warning("Improve your resume using the suggestions above to reach a 100% ATS score!")
                    else:
                        st.success("Congratulations! Your resume is fully optimized for ATS.")
                else:
                    st.info("ATS Score not detected. Please review the AI suggestions above.")

                st.download_button("💾 Download Enhanced Resume", clean_text, file_name="enhanced_resume.txt")
            except Exception as e:
                st.error(f"AI error: {e}")

def get_demo_jobs(keywords, location, num_results=10):
    """Simulate fetching latest jobs from trusted portals (demo, no API)"""
    platforms = [
        {"name": "LinkedIn", "url": "https://www.linkedin.com/jobs/", "logo": "https://cdn-icons-png.flaticon.com/512/174/174857.png"},
        {"name": "Indeed", "url": "https://www.indeed.com/jobs/", "logo": "https://cdn-icons-png.flaticon.com/512/732/732220.png"},
        {"name": "Naukri", "url": "https://www.naukri.com/", "logo": "https://static.naukimg.com/s/4/100/i/naukri_Logo.png"},
        {"name": "Monster", "url": "https://www.monsterindia.com/", "logo": "https://media.monsterindia.com/trex/public/default/images/monster-logo.svg"},
        {"name": "Glassdoor", "url": "https://www.glassdoor.co.in/Job/", "logo": "https://cdn-icons-png.flaticon.com/512/5968/5968534.png"}
    ]
    demo_titles = [
        "Software Engineer", "Data Analyst", "AI Research Intern", "Frontend Developer",
        "Backend Developer", "Cloud Engineer", "Business Analyst", "DevOps Engineer",
        "Product Manager", "QA Engineer", "UI/UX Designer", "Cybersecurity Analyst", "AI Engineer"
    ]
    demo_companies = [
        {"name": "TechNova", "logo": "https://logo.clearbit.com/technova.com"},
        {"name": "DataCo", "logo": "https://logo.clearbit.com/dataco.com"},
        {"name": "InnovateAI", "logo": "https://logo.clearbit.com/innovateai.com"},
        {"name": "Cloudify", "logo": "https://logo.clearbit.com/cloudify.com"},
        {"name": "BizAnalytics", "logo": "https://logo.clearbit.com/bizanalytics.com"},
        {"name": "FinEdge", "logo": "https://logo.clearbit.com/finedge.com"},
        {"name": "HealthPlus", "logo": "https://logo.clearbit.com/healthplus.com"},
    ]
    demo_locations = [
        "Remote", "Bangalore", "Hyderabad", "Delhi", "Mumbai", "Pune", "Chennai", "Gurgaon", "Delhi NCR", "Delhi gurugoan"
    ]
    demo_skills = ["Python", "SQL", "Machine Learning", "React", "AWS", "Excel", "Docker", "Java", "C++", "Kubernetes", "Remote", "AI Engineer"]

    jobs = []
    user_keywords = [k.strip().lower() for k in (keywords.split(",") if keywords else []) if k.strip()]
    user_locations = [l.strip().lower() for l in (location.split(",") if location else []) if l.strip()]

    # Add user locations to possible locations for more flexibility
    possible_locations = demo_locations.copy()
    for uloc in user_locations:
        if uloc and uloc not in [l.lower() for l in demo_locations]:
            possible_locations.append(uloc)

    for i in range(num_results * 5):  # Generate more for better filtering
        title = random.choice(demo_titles)
        company = random.choice(demo_companies)
        loc = random.choice(possible_locations)
        skill = random.choice(demo_skills)
        platform = random.choice(platforms)
        posted_at = (datetime.utcnow() - timedelta(hours=random.randint(1, 23))).strftime("%Y-%m-%d %H:%M")

        # Enhanced: Accept any location(s) (partial match, multi-location)
        if user_locations:
            if not any(uloc in loc.lower() for uloc in user_locations):
                continue

        # Enhanced: Accept any job keyword(s) (partial match, multi-keyword)
        if user_keywords:
            match = False
            for kw in user_keywords:
                if kw in title.lower() or kw in skill.lower():
                    match = True
                    break
            if not match:
                continue

        jobs.append({
            "job_title": title,
            "employer_name": company["name"],
            "company_logo": company["logo"],
            "job_city": loc,
            "job_country": "India",
            "job_salary": f"₹{random.randint(4, 40)} LPA",
            "job_posted_at_datetime_utc": posted_at,
            "job_description": f"{title} role at {company['name']} requiring {skill}. Work on real projects with top teams. Apply now for a trusted opportunity!",
            "job_apply_link": f"{platform['url']}search?q={title.replace(' ', '+')}",
            "platform": platform["name"],
            "platform_logo": platform["logo"]
        })
        if len(jobs) >= num_results:
            break

    return jobs

def job_matching_tab():
    st.markdown('''
        <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 class="title-glow">🔔 Personalized Job Alerts</h1>
            <p style="color: #43e97b; font-size: 1.2rem;">
                Get instant, personalized job recommendations from your favorite portals.<br>
                <span style="color:#10B981;">🎯 Enter your preferences and get the latest jobs!</span>
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # Enhanced interactive input fields
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-size:1.1rem;color:#ffb86b;'>🎯 Enter Job Title</span>
    </div>
    """, unsafe_allow_html=True)
    job_title = st.text_input("Job Title", placeholder="e.g., Data Scientist, Software Engineer")
    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-size:1.1rem;color:#ffb86b;'>📍 Preferred Location</span>
    </div>
    """, unsafe_allow_html=True)
    location = st.text_input("Preferred Location", placeholder="e.g., Remote, New York, Bangalore")

    st.markdown("""
    <div style='margin-bottom:1.5rem;'>
        <span style='font-size:1.1rem;color:#ffb86b;'>Select Job Sources</span>
    </div>
    """, unsafe_allow_html=True)
    sources = st.multiselect(
        "Job Sources",
        ["🟢 Indeed Jobs", "🔵 LinkedIn Jobs", "🟠 Naukri Jobs", "🔴 Google Jobs"],
        default=["🟢 Indeed Jobs", "🔵 LinkedIn Jobs", "🟠 Naukri Jobs", "🔴 Google Jobs"]
    )

    # Sidebar for saved/applied jobs
    if 'saved_jobs' not in st.session_state:
        st.session_state['saved_jobs'] = []
    if 'applied_jobs' not in st.session_state:
        st.session_state['applied_jobs'] = []

    with st.sidebar:
        st.markdown("<h4 style='color:#43e97b;'>💾 Saved Jobs</h4>", unsafe_allow_html=True)
        if st.session_state['saved_jobs']:
            for job in st.session_state['saved_jobs']:
                st.markdown(f"- <b>{job['job_title']}</b> at {job['employer_name']}", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#aaa;'>No jobs saved yet.</span>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#ffb86b;'>✅ Applied Jobs</h4>", unsafe_allow_html=True)
        if st.session_state['applied_jobs']:
            for job in st.session_state['applied_jobs']:
                st.markdown(f"- <b>{job['job_title']}</b> at {job['employer_name']}", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#aaa;'>No jobs marked as applied.</span>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin:1.5rem 0;'>
        <span style='font-size:1.1rem;color:#43e97b;'>Upload your resume for even better matching!</span>
    </div>
    """, unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("Upload your resume (PDF, DOCX)", type=["pdf", "docx"])

    if st.button("Find Latest Personalized Jobs", use_container_width=True):
        with st.spinner("Fetching personalized jobs from selected sources..."):
            # Use job_title and location for demo jobs
            keywords = job_title
            # Simulate source filtering (for demo, all sources return same jobs)
            jobs = get_demo_jobs(keywords, location, num_results=20)
            # Filter by selected sources (simulate)
            filtered_jobs = []
            for job in jobs:
                if ("🟢 Indeed Jobs" in sources and job['platform'] == "Indeed") or \
                   ("🔵 LinkedIn Jobs" in sources and job['platform'] == "LinkedIn") or \
                   ("🟠 Naukri Jobs" in sources and job['platform'] == "Naukri") or \
                   ("🔴 Google Jobs" in sources and job['platform'] == "Google"):
                    filtered_jobs.append(job)
            if not filtered_jobs:
                st.warning("No jobs found for the selected sources. Try changing your filters.")
            else:
                st.markdown("### 🚀 <span style='color:#10B981;'>Latest Personalized Jobs</span>", unsafe_allow_html=True)
                for idx, job in enumerate(filtered_jobs):
                    job_id = f"{job['job_title']}_{job['employer_name']}_{idx}"
                    is_saved = any(j['job_title'] == job['job_title'] and j['employer_name'] == job['employer_name'] for j in st.session_state['saved_jobs'])
                    is_applied = any(j['job_title'] == job['job_title'] and j['employer_name'] == job['employer_name'] for j in st.session_state['applied_jobs'])
                    with st.container():
                        col1, col2 = st.columns([8,2])
                        with col1:
                            st.markdown(f"""
<div class='glass-card' style='margin-bottom:1.5rem; display:flex; align-items:center;'>
    <img src="{job.get('company_logo','')}" alt="logo" style="width:48px;height:48px;border-radius:8px;vertical-align:middle;margin-right:16px;box-shadow:0 0 8px #06B6D4;">
    <div style="flex:1;">
        <b style="font-size:1.1rem;">{job.get('job_title', 'Job Title')}</b> at <b>{job.get('employer_name', 'Company')}</b>
        <br>📍 <b>{job.get('job_city', '')}, {job.get('job_country', '')}</b>
        <br>💰 <b>{job.get('job_salary', 'N/A')}</b>
        <br>🕒 <span style="color:#10B981;">Posted: {job.get('job_posted_at_datetime_utc', '')}</span>
        <br><span style="color:#06B6D4;">{job.get('job_description', '')[:180]}...</span>
        <br>
        <span style="display:inline-flex;align-items:center;margin-top:8px;">
            <img src="{job.get('platform_logo','')}" alt="platform" style="width:22px;height:22px;border-radius:4px;margin-right:6px;">
            <b style="color:#818CF8;">{job.get('platform')}</b>
        </span>
        <a href="{job.get('job_apply_link', '#')}" target="_blank" style="margin-left:18px;">
            <button style="background:#10B981;color:#fff;border:none;padding:8px 20px;border-radius:6px;margin-top:8px;font-weight:600;box-shadow:0 0 8px #10B981;cursor:pointer;">
                Apply Now
            </button>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
                            with st.expander("View Details"):
                                st.markdown(f"<b>Full Description:</b><br>{job.get('job_description','')}", unsafe_allow_html=True)
                                st.markdown(f"<b>Platform:</b> {job.get('platform')}<br><b>Posted:</b> {job.get('job_posted_at_datetime_utc','')}", unsafe_allow_html=True)
                        with col2:
                            if not is_saved:
                                if st.button("💾 Save Job", key=f"save_{job_id}"):
                                    st.session_state['saved_jobs'].append(job)
                                    st.success(f"Saved: {job['job_title']} at {job['employer_name']}")
                            else:
                                st.markdown("<span style='color:#43e97b;font-weight:700;'>Saved ✔️</span>", unsafe_allow_html=True)
                            if not is_applied:
                                if st.button("✅ Mark as Applied", key=f"applied_{job_id}"):
                                    st.session_state['applied_jobs'].append(job)
                                    st.success(f"Marked as applied: {job['job_title']} at {job['employer_name']}")
                            else:
                                st.markdown("<span style='color:#ffb86b;font-weight:700;'>Applied ✔️</span>", unsafe_allow_html=True)
                st.success("All jobs above are from trusted, verified portals. Click 'Apply Now' to go directly to the official job page.")

    st.markdown("""
        <div style="margin-top:2rem;text-align:center;">
            <span style="color:#818CF8;font-size:13px;">
                Data is simulated for demo. For 100% real jobs, always apply on the official portal.<br>
                <b>Tip:</b> Use specific keywords (e.g., 'React Developer', 'Remote Python') for best results.
            </span>
        </div>
    """, unsafe_allow_html=True)
def interview_and_career_tab():
    st.markdown('''
        <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 class="title-glow">🤖 INTERVIEW PREPARATION & CAREER PATH</h1>
            <p style="color: #06B6D4;">Practice interviews, get AI feedback, and discover your next career move!</p>
        </div>
    ''', unsafe_allow_html=True)

    st.header("1️⃣ Mock Interview Q&A")
    uploaded_resume = st.file_uploader("Upload your resume (PDF, DOC, DOCX) for interview questions", type=["pdf", "doc", "docx"], key="interview_resume")
    job_desc = st.text_area("Paste the target job description (optional)", key="interview_jobdesc")
    num_questions = st.slider("Number of questions", 3, 10, 5)
    
    if st.button("Generate Interview Questions", key="gen_interview_qs"):
        if uploaded_resume:
            with st.spinner("Extracting resume and generating questions..."):
                resume_text = ATSAnalyzer.extract_text(uploaded_resume)
                prompt = f"""
You are an expert interviewer. Based on the following resume and job description, generate {num_questions} personalized interview questions. Focus on technical, behavioral, and situational aspects relevant to the job.

Resume:
{resume_text}

Job Description:
{job_desc}
"""
                try:
                    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                    response = model.generate_content(prompt)
                    questions = [q.strip() for q in response.text.split("\n") if q.strip()]
                    st.session_state["mock_questions"] = questions
                    st.success("Questions generated! Answer below for AI feedback.")
                except Exception as e:
                    st.error(f"AI error: {e}")
        else:
            st.warning("Please upload your resume.")

    if "mock_questions" in st.session_state:
        st.markdown("### 📝 Your Interview Practice")
        answers = []
        for idx, q in enumerate(st.session_state["mock_questions"]):
            ans = st.text_area(f"Q{idx+1}: {q}", key=f"answer_{idx}")
            answers.append(ans)
        if st.button("Get AI Feedback on Answers", key="ai_feedback_btn"):
            with st.spinner("Analyzing your answers..."):
                feedback_prompt = f"""
You are an expert interview coach. For each question and answer below, provide constructive feedback and suggestions for improvement. Be specific and actionable.

"""
                for i, q in enumerate(st.session_state["mock_questions"]):
                    feedback_prompt += f"Q{i+1}: {q}\nA: {answers[i]}\n"
                try:
                    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                    feedback = model.generate_content(feedback_prompt)
                    st.markdown("### 🤖 AI Feedback")
                    st.markdown(f"<div class='glass-card'><pre>{feedback.text}</pre></div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI error: {e}")

    st.markdown("---")
    st.header("2️⃣ Career Path Recommendation & Roadmap")
    uploaded_resume2 = st.file_uploader("Upload your resume (PDF, DOC, DOCX) for career path", type=["pdf", "doc", "docx"], key="career_resume")
    job_goal = st.text_input("Target Job Role (Optional)", key="career_goal")
    if st.button("Suggest Career Paths & Roadmap", key="career_path_btn"):
        if uploaded_resume2:
            with st.spinner("Analyzing your resume and suggesting career paths..."):
                resume_text = ATSAnalyzer.extract_text(uploaded_resume2)
                prompt = f"""
You are a career coach. Analyze the following resume{f' and the target job role: {job_goal}' if job_goal else ''}. Suggest 2-3 suitable career paths or roles, and for each, provide a step-by-step roadmap (skills/certifications/learning) to reach that role. Format as:

Career Path: <Role>
Why Suitable: <Reason>
Roadmap:
1. <Step 1>
2. <Step 2>
...

Resume:
{resume_text}
"""
                try:
                    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                    response = model.generate_content(prompt)
                    st.markdown("### 🚀 Career Path Recommendations & Roadmap")
                    st.markdown(f"<div class='glass-card'><pre>{response.text}</pre></div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI error: {e}")
        else:
            st.warning("Please upload your resume.")

def current_job_section():
    st.header("Current Jobs")
    if 'current_jobs' not in st.session_state:
        st.session_state.current_jobs = []
    if 'edit_index' not in st.session_state:
        st.session_state.edit_index = None

    def reset_form():
        st.session_state['job_title'] = ''
        st.session_state['company'] = ''
        st.session_state['start_date'] = datetime.date.today()
        st.session_state['description'] = ''
        st.session_state['skills'] = ''
        st.session_state['document'] = None
        st.session_state['edit_index'] = None

    # Job Form
    with st.expander("Add New Current Job", expanded=False):
        st.text_input("Job Title", key='job_title')
        st.text_input("Company", key='company')
        st.date_input("Start Date", key='start_date')
        st.text_area("Description", key='description')
        st.text_input("Skills Used (comma separated)", key='skills')
        st.file_uploader("Upload Related Document (optional)", key='document')
        if st.button("Save Job"):
            job = {
                'title': st.session_state['job_title'],
                'company': st.session_state['company'],
                'start_date': st.session_state['start_date'],
                'description': st.session_state['description'],
                'skills': st.session_state['skills'],
                'document': st.session_state['document'].name if st.session_state['document'] else None
            }
            if st.session_state['edit_index'] is not None:
                st.session_state.current_jobs[st.session_state['edit_index']] = job
            else:
                st.session_state.current_jobs.append(job)
            reset_form()
            st.success("Job saved!")

    # Display Current Jobs
    st.subheader("Your Current Jobs")
    if st.session_state.current_jobs:
        for idx, job in enumerate(st.session_state.current_jobs):
            with st.container():
                st.markdown(f"**{job['title']}** at **{job['company']}**")
                st.markdown(f"Start Date: {job['start_date']}")
                st.markdown(f"Description: {job['description']}")
                st.markdown(f"Skills: {job['skills']}")
                if job['document']:
                    st.markdown(f"[Download Document](/{job['document']})")
                col1, col2 = st.columns(2)
                if col1.button("Edit", key=f"edit_{idx}"):
                    st.session_state['job_title'] = job['title']
                    st.session_state['company'] = job['company']
                    st.session_state['start_date'] = job['start_date']
                    st.session_state['description'] = job['description']
                    st.session_state['skills'] = job['skills']
                    st.session_state['edit_index'] = idx
                if col2.button("Delete", key=f"delete_{idx}"):
                    st.session_state.current_jobs.pop(idx)
                    st.success("Job deleted!")
                    st.experimental_rerun()
    else:
        st.info("No current jobs added yet.")

# --- Main App ---
def main():
    # Theme configuration
    st.markdown("""
        <style>
        /* Ultra-modern, playful, and interactive color palette */
        :root {
            --primary: #ff6f61;  /* Coral */
            --primary-light: #ffb86b; /* Peach */
            --accent: #43e97b;   /* Green-Teal */
            --accent2: #38a1db;  /* Sky Blue */
            --accent3: #a259f7;  /* Purple */
            --accent4: #fcb045;  /* Orange */
            --success: #43e97b;  /* Green-Teal */
            --warning: #fcb045;  /* Orange */
            --error: #ff6f61;    /* Coral */
            --dark-bg: #18122b;  /* Deep Purple */
            --card-bg: rgba(24, 18, 43, 0.92);
            --glass-bg: rgba(255,255,255,0.08);
            --neon-glow: 0 0 18px #ffb86b, 0 0 32px #43e97b, 0 0 24px #a259f7;
        }

        /* Animated rainbow gradient background */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(120deg, #ff6f61 0%, #ffb86b 20%, #43e97b 40%, #38a1db 60%, #a259f7 80%, #fcb045 100%);
            opacity: 0.25;
            z-index: -2;
            animation: rainbowBG 18s ease-in-out infinite;
            background-size: 300% 300%;
        }
        @keyframes rainbowBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Glassmorphism cards with playful border */
        .glass-card {
            background: var(--card-bg) !important;
            border: 2.5px solid transparent !important;
            border-radius: 28px !important;
            backdrop-filter: blur(22px) !important;
            box-shadow: 0 0 40px 0 #a259f755, 0 0 18px 0 #43e97b55 !important;
            transition: all 0.3s;
            position: relative;
        }
        .glass-card:after {
            content: '';
            position: absolute;
            inset: 0;
            border-radius: 28px;
            padding: 2px;
            background: linear-gradient(120deg, #ffb86b, #43e97b, #a259f7, #fcb045);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            pointer-events: none;
            z-index: 1;
        }
        .glass-card:hover {
            box-shadow: 0 0 60px 0 #ffb86bcc, 0 0 32px 0 #a259f7cc !important;
        }

        /* Rainbow neon title */
        h1, .title-glow {
            color: #fff !important;
            text-shadow: 0 0 24px #ffb86b, 0 0 48px #a259f7, 0 0 32px #43e97b !important;
            background: linear-gradient(90deg, #ff6f61, #ffb86b, #43e97b, #38a1db, #a259f7, #fcb045);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900 !important;
            letter-spacing: 2.5px;
            animation: titleRainbow 6s linear infinite alternate;
        }
        @keyframes titleRainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }

        /* Futuristic, colorful inputs */
        .stTextArea textarea, .stTextInput input {
            background: var(--glass-bg) !important;
            border: 2.5px solid #a259f7 !important;
            border-radius: 16px !important;
            color: #fff !important;
            font-size: 1.12em !important;
            transition: all 0.3s;
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #43e97b !important;
            box-shadow: 0 0 22px #43e97b !important;
        }

        /* Rainbow glowing buttons */
        .stButton > button {
            background: linear-gradient(90deg, #ff6f61, #ffb86b, #43e97b, #38a1db, #a259f7, #fcb045) !important;
            border: none !important;
            color: #18122b !important;
            font-weight: 900 !important;
            border-radius: 12px !important;
            font-size: 1.12em !important;
            box-shadow: 0 0 22px #a259f7, 0 0 10px #43e97b !important;
            transition: all 0.2s;
            letter-spacing: 1.2px;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #fcb045, #a259f7, #38a1db, #43e97b, #ffb86b, #ff6f61) !important;
            color: #fff !important;
            box-shadow: 0 0 44px #43e97b, 0 0 22px #ffb86b !important;
        }

        /* Progress bar with rainbow gradient */
        .stProgress > div > div {
            background: linear-gradient(90deg, #ff6f61, #ffb86b, #43e97b, #38a1db, #a259f7, #fcb045) !important;
        }

        /* Sidebar with rainbow accent and more contrast */
        .css-1d391kg {
            background: linear-gradient(180deg, #18122b 0%, #ff6f61 20%, #43e97b 50%, #a259f7 80%, #fcb045 100%) !important;
            border-right: 3px solid #ffb86b !important;
        }

        /* Neon effect for subheaders and labels */
        .subheader, .stSelectbox label, .stTextArea label, .stFileUploader label, .stRadio > label, .stMultiSelect > label, .streamlit-expanderHeader {
            color: #ffb86b !important;
            text-shadow: 0 0 12px #a259f7 !important;
            font-weight: 800 !important;
        }
        h2, h3, h4 {
            color: #43e97b !important;
            text-shadow: 0 0 12px #ffb86b !important;
        }

        /* Success, warning, error messages */
        .success-message, .element-container div.stMarkdown p.success-message {
            color: #43e97b !important;
            text-shadow: 0 0 12px #ffb86b !important;
        }
        .stWarning {
            background: rgba(252, 176, 69, 0.18) !important;
            border: 2.5px solid #fcb045 !important;
            color: #18122b !important;
        }
        .stError {
            background: rgba(255, 111, 97, 0.18) !important;
            border: 2.5px solid #ff6f61 !important;
            color: #fff !important;
        }

        /* Markdown/pre blocks */
        .element-container div.stMarkdown pre {
            background: rgba(24, 18, 43, 0.98) !important;
            border: 2.5px solid #a259f7 !important;
            color: #ffb86b !important;
            font-size: 1.12em !important;
            border-radius: 16px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; margin-bottom: 20px;'>
                <h1 class='title-glow' style='margin: 0; font-size: 26px;'>CAREERCRAFT JOB.AI</h1>
                <p style='margin: 0; background: linear-gradient(120deg, #818CF8, #67E8F9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 11px; text-transform: uppercase; letter-spacing: 2px;'>
                    Smart fusion of Gemini and Groq API's
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Page Selection with cool icons
        page = st.radio("NAVIGATE",[
            "Smart Resume Analyzer", "AI Resume Builder", "Job Matching", "Smart Cold Mail Generator", "Interview Prep & Career Path", "Career Chatbot", "Interactive Resume Editor", "Current Jobs"],
            format_func=lambda x: f"📄 {x}" if x == "Smart Resume Analyzer" else f"🛠️ {x}" if x == "AI Resume Builder" else f"🔎 {x}" if x == "Job Matching" else f"✉️ {x}" if x == "Smart Cold Mail Generator" else ("🤖 " + x if x == "Interview Prep & Career Path" else ("💬 " + x if x == "Career Chatbot" else "📝 " + x)))
        
        # Language selector only for Resume Analyzer
        selected_language = "English"  # Default language for Cold Mail
        if page == "Smart Resume Analyzer":
            # Language selector with modern flags
            language = st.selectbox("🌐 Select Language",
                ["🇺🇸 English","🇮🇳 हिंदी","🇮🇳 తెలుగు"],index=0,
                help="Choose your preferred language for analysis")

            # Update language mapping
            language_mapping = {"🇺🇸 English": "English","🇮🇳 हिंदी": "हिंदी","🇮🇳 తెలుగు": "తెలుగు"}
            
            # Get the actual language key for prompts
            selected_language = language_mapping[language]

        if page == "Smart Resume Analyzer": 
            st.markdown("<p style='color: #0066cc; margin-top: 20px;'>Choose your preferred Analysis Type</p>", unsafe_allow_html=True)
            # Analysis type selector with cool badges
            analysis_types = st.multiselect("SELECT ANALYSIS MODULES",
                list(ATSAnalyzer.ANALYSIS_TYPES.keys()),
                default=["Complete Analysis"],
                format_func=lambda x: f"{'🔍' if 'Complete' in x else '🎯' if 'Skills' in x else '🤖' if 'ATS' in x else '📊'} {x}")
            
            # Model selection with tech badges
            model_choice = st.selectbox("SELECT AI MODEL",
                list(ATSAnalyzer.AI_MODELS.keys()),
                format_func=lambda x: ATSAnalyzer.AI_MODELS[x])
        else:
            st.markdown("<p style='color: #0066cc; margin-top: 20px;'>Choose your preferred AI MODEL</p>", unsafe_allow_html=True)
            
            # Model selection for cold mail
            model_choice = st.selectbox("SELECT AI MODEL",
                list(ATSAnalyzer.AI_MODELS.keys()),
                format_func=lambda x: ATSAnalyzer.AI_MODELS[x])

    # Get language-specific labels
    labels = ATSAnalyzer.LANGUAGE_PROMPTS[selected_language]["labels"] if page == "Smart Resume Analyzer" else ATSAnalyzer.LANGUAGE_PROMPTS["English"]["labels"]
    
    if page == "Smart Resume Analyzer":
        # Futuristic Header for Resume Analyzer
        st.markdown('''
            <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
                <h1 class="title-glow">📄AWESOME RESUME ANALYZER.AI</h1>
                <p style="color: #0066cc; text-transform: uppercase; letter-spacing: 2px;">
                    🎯 Smart Analysis • 🔍 Deep Insights • ⚡ Quick Results
                </p>
            </div>
        ''', unsafe_allow_html=True)
        
        # Resume Analyzer page content
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("📝 Job Description Details")
            job_title = st.text_input("Job Title (Optional)", placeholder="e.g., Software Engineer (optional)")
            job_description = st.text_area("Job Description",
                height=200,
                placeholder="Paste the job description here...")

        with col2:
            st.subheader("📄 Your Resume")
            uploaded_file = st.file_uploader("Upload your resume (PDF, DOC, DOCX)",
                type=["pdf", "doc", "docx"])

            if uploaded_file:
                st.markdown(f'<p class="success-message">✅ {uploaded_file.name} uploaded successfully!</p>', unsafe_allow_html=True)

        # Analysis section
        if uploaded_file and job_description and analysis_types:
            if st.button(labels["analyze"], use_container_width=True):
                doc_text = ATSAnalyzer.extract_text(uploaded_file)
                
                if doc_text:
                    for analysis_type in analysis_types:
                        with st.spinner(f"Performing {analysis_type}..."):
                            # Get analysis prompt
                            analysis_prompt = ATSAnalyzer.ANALYSIS_TYPES[analysis_type]
                            
                            # Get response
                            response = ATSAnalyzer.get_ai_response(model_choice,analysis_prompt,doc_text,job_description,selected_language)
                            
                            if response:
                                # Use the class method instead of global function
                                analysis_data = ATSAnalyzer.extract_data_from_response(response)
                                if analysis_data:
                                    st.markdown("## 📊 Analysis Results")
                                    
                                    
                                    # Display analysis results in text format
                                    st.markdown("### 📝 Detailed Analysis")
                                    st.markdown(response)
                    
                    # Download button for complete analysis
                    st.download_button("📥 Download Complete Analysis",
                        "\n\n".join([f"=== {at} ===\n{ATSAnalyzer.get_ai_response(model_choice, ATSAnalyzer.ANALYSIS_TYPES[at], doc_text, job_description, selected_language)}" for at in analysis_types]),
                        file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain")

    elif page == "AI Resume Builder":
        ai_resume_builder_tab()
    elif page == "Job Matching":
        job_matching_tab()
    elif page == "Current Jobs":
        current_job_section()
    else:
        # Futuristic Header for Cold Mail Generator
        st.markdown('''
            <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
                <h1 class="title-glow">✉️ SMART COLD MAIL GENERATOR</h1>
                <p style="color: #0066cc; text-transform: uppercase; letter-spacing: 2px;">
                    💼 Professional • 🎯 Targeted • ✨ Impactful
                </p>
            </div>''', unsafe_allow_html=True)
        
        # Create two columns for inputs
        col1, col2 = st.columns(2)
        
        with col1:
            # Job Description Input
            st.subheader("📝 Job Description Detail")
            job_description = st.text_area(
                "Job description",
                height=300,
                placeholder="Paste the complete job description to generate a tailored cold mail..."
            )
        
        with col2:
            # Resume Upload
            st.markdown("### 📄 Your Resume")
            uploaded_resume = st.file_uploader("Upload your resume",
                type=["pdf", "doc", "docx"],
                help="Upload your resume to personalize the cold mail")
            
            if uploaded_resume:
                st.success(f"✅ Resume uploaded: {uploaded_resume.name}")
        
        # Cold Mail Type Selection with descriptions
        st.markdown("### 📋 Select Cold Mail Style")
        cold_mail_type = st.selectbox("Choose your preferred style",
            list(ATSAnalyzer.COLD_MAIL_TYPES.keys()),
            format_func=lambda x: f"{x} - {ATSAnalyzer.COLD_MAIL_TYPES[x]['description']}")

        # Personal Information
        with st.expander("✍🏽Enter Your Personal Information (Optional)"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Your Full Name", placeholder="Your Name")
                email = st.text_input("Email Address", placeholder="YourName@email.com")
                university = st.text_input("University/College Name", placeholder="Your University/College Name")
                
            with col2:
                phone = st.text_input("Phone Number", placeholder="98XXXXXXXX")
                linkedin = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/yourusername")
                degree = st.text_input("Degree & Year", placeholder="3rd Year, B.Sc.Stream")

        # Generate Button
        if uploaded_resume and job_description:
            if st.button("Generate Cold Mail", use_container_width=True):
                doc_text = ATSAnalyzer.extract_text(uploaded_resume)
                
                if doc_text:
                    with st.spinner("📨 Crafting your personalized cold mail..."):
                        # Get the selected template
                        template = ATSAnalyzer.COLD_MAIL_TYPES[cold_mail_type]["template"]
                        
                        # Generate cold mail
                        cold_mail = ATSAnalyzer.generate_cold_mail(
                            model_choice=model_choice,
                            prompt=template,
                            resume_text=doc_text,
                            job_description=job_description,
                            personal_info={"name": name,
                                "email": email,
                                "phone": phone,
                                "university": university,
                                "linkedin": linkedin,
                                "degree": degree})
                        
                        if cold_mail:
                            st.markdown("### 📧 Your Generated Cold Mail")
                            st.markdown('''
                                <div class="glass-card" style="padding: 2rem; margin-top: 1rem;">
                                    <pre style="white-space: pre-wrap; word-wrap: break-word;">{}</pre>
                                </div>
                            '''.format(cold_mail), unsafe_allow_html=True)
                            
                            # Download button
                            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"cold_mail_{current_time}.txt"
                            
                            st.download_button(label="💾 Download Cold Mail",
                                data=cold_mail,
                                file_name=filename,
                                mime="text/plain",
                                use_container_width=True)
        
    if page == "Interview Prep & Career Path":
        interview_and_career_tab()
    if page == "Career Chatbot":
        st.markdown('''
                <div class="cyber-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
                    <h1 class="title-glow">💬 Career Guidance Chatbot</h1>
                    <p style="color: #06B6D4;">Ask anything about job search, resume tips, interview prep, or career advice!</p>
                </div>
            ''', unsafe_allow_html=True)
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        if "_waiting_for_response" not in st.session_state:
            st.session_state["_waiting_for_response"] = False
        if "_input_sent" not in st.session_state:
            st.session_state["_input_sent"] = False
        if "chatbot_input" not in st.session_state:
            st.session_state["chatbot_input"] = ""

        use_chat_message = hasattr(st, "chat_message")

        # Clear chat button
        col1, col2 = st.columns([4,1])
        with col2:
            if st.button("🧹 Clear Chat", use_container_width=True):
                st.session_state["chat_history"] = []
                st.session_state["_input_sent"] = False
                st.session_state["chatbot_input"] = ""
                st.session_state["_waiting_for_response"] = False
                st.experimental_rerun()

        st.markdown("## 💬 Smart Job Assistant Chat")
        chat_placeholder = st.container()
        with chat_placeholder:
            if st.session_state["chat_history"]:
                if use_chat_message:
                    for q, a in st.session_state["chat_history"]:
                        with st.chat_message("user"):
                            st.markdown(f"""
<div class='chat-bubble-user'>
    <b>You:</b> {q}
</div>
""", unsafe_allow_html=True)
                        with st.chat_message("assistant"):
                            st.markdown(f"""
<div class='chat-bubble-ai'>
    <b>AI:</b> {a}
</div>
""", unsafe_allow_html=True)
                else:
                    st.markdown("### 🗨️ Chat History")
                    for q, a in st.session_state["chat_history"]:
                        st.markdown(f"""
<div class='chat-bubble-user'>
    <b>You:</b> {q}
</div>
""", unsafe_allow_html=True)
                        st.markdown(f"""
<div class='chat-bubble-ai'>
    <b>AI:</b> {a}
</div>
""", unsafe_allow_html=True)
            # Typing indicator
            if st.session_state.get("_waiting_for_response", False):
                st.markdown("<div style='color:#888;font-style:italic;margin-bottom:8px;'>AI is typing...</div>", unsafe_allow_html=True)

        def build_chat_prompt(history, user_message):
            prompt = "You are a friendly, helpful, and expert career assistant. Hold a natural, human-like conversation. Remember the chat history and respond as if you are talking one-to-one.\n\n"
            for i, (q, a) in enumerate(history):
                prompt += f"User: {q}\nAI: {a}\n"
            prompt += f"User: {user_message}\nAI:"
            return prompt

        # Only allow new input if not currently processing
        if not st.session_state.get("_waiting_for_response", False):
            user_input = st.text_input(
                "Type your question here...",
                key="chatbot_input",
                placeholder="Ask me anything about your career...",
                on_change=None
            )
            send_btn = st.button("Send", use_container_width=True)
        else:
            user_input = st.session_state.get("chatbot_input", "")
            send_btn = False

        # Only process if not waiting and input is present
        if (user_input and send_btn) or (user_input and not send_btn and st.session_state.get("_input_sent", False) == False):
            st.session_state["_input_sent"] = True
            st.session_state["_waiting_for_response"] = True
            with st.spinner("Thinking..."):
                try:
                    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
                    chat_prompt = build_chat_prompt(st.session_state["chat_history"], user_input)
                    response = model.generate_content(chat_prompt)
                    st.session_state["chat_history"].append((user_input, response.text))
                except Exception as e:
                    st.session_state["chat_history"].append((user_input, f"[AI error: {e}]") )
            st.session_state["chatbot_input"] = ""
            st.session_state["_waiting_for_response"] = False
            st.experimental_rerun()
        else:
            st.session_state["_input_sent"] = False

        # Auto-scroll to latest message (Streamlit chat_message does this natively)
        if st.session_state["chat_history"] and not use_chat_message:
            st.markdown("<div id='bottom'></div>", unsafe_allow_html=True)
            st.markdown("""
                <script>
                    var bottom = document.getElementById('bottom');
                    if (bottom) bottom.scrollIntoView({behavior: 'smooth'});
                </script>
            """, unsafe_allow_html=True)

    # Footer with futuristic style
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <div style='color: #0066cc; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;'>
                ⚠️ AI can make mistakes.Please Double Check the Response
            </div>
            <div style='font-size: 10px; color: rgba(255,255,255,0.7);'>
                💼 Smart Job Assistant • © 2025 Abhishek Kumar. All rights reserved.
            </div>
               </div>
        """,
        unsafe_allow_html=True)

if __name__ == "__main__":
    main()