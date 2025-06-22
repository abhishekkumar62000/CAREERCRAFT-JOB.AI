![fromtend](https://github.com/user-attachments/assets/ddf84002-9626-4584-909e-bb763f83a004)
![fromtend1](https://github.com/user-attachments/assets/d7fecf3f-2b3f-4305-941d-b696692a06dc)

<h1 align="center">🚀 CAREERCRAFT JOB.AI – Smart Job Assistant 🤖</h1>

## 🌐 Live App🔗 **[Launch CAREERCRAFT JOB.AI](https://careercraft-job-ai.streamlit.app/)**

<p align="center">
  <b>AI-Powered Career Companion for Smarter Job Search, Resume Analysis & Interview Prep</b><br>
  <a href="https://your-app-link.streamlit.app" target="_blank">🌐 Live App Coming Soon!</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-UI-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/NLP%20Powered-Yes-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Career%20Tools-Resume|Jobs|Interview-orange?style=for-the-badge" />
</p>

---

## 🧠 Overview

**CAREERCRAFT JOB.AI** is an AI-driven web app designed to help job seekers **analyze resumes, explore job recommendations, prepare for interviews, and understand skill gaps**.

With the power of **Streamlit**, **Natural Language Processing (NLP)**, and **data visualization**, this app acts as your **all-in-one career assistant**.

---

## 🚀 Key Features

### 🖥️ Streamlit UI with Smart Navigation
- Interactive and modern UI built with Streamlit
- Sidebar navigation for quick access to:
  - Resume Analyzer 📄
  - Job Recommender 💼
  - Interview Prep 🎙️
  - Skill Gap Analysis 📉
  - Market Insights 📊

---



---




---

## 🎯 Purpose & Vision

CAREERCRAFT JOB.AI is crafted to be a **comprehensive, intelligent career assistant**—supporting users across every stage of the job-seeking process:

* **Resume analysis** with feedback on skills, experience, and formatting
* **Job recommendation engine** powered by NLP and keyword matching
* **Interview prep** via AI-generated questions tailored to your background and target roles
* **Skill gap analysis** identifying missing competencies and offering learning paths
* **Job market insights** such as salary ranges, role demand, and qualification trends
* **Downloadable personalized reports** to track and apply actionable feedback

Its goal: **empower individuals to strategically prepare, apply, interview, and grow in an evolving job market.**

---

## 🧭 Feature Walkthrough

### 1. 🖥️ Streamlit-Powered User Interface

* **Sidebar navigation** enables seamless switching between modules
* Clean layout: upload panels, visualizations, analysis text blocks
* Reactive feedback: adjusts recommendations as inputs change

---

### 2. 📄 Resume Analyzer

* Handles **PDF** and plain **text** formats
* Uses **PyMuPDF** (for PDF parsing) or Python file I/O
* Applies **spaCy** (or optionally **NLTK**) to:

  * Parse named entities, education, work experience dates
  * Identify hard & soft skills with matching skill databases
* Outputs:

  * Highlighted **skills overview**
  * **Experience evaluation** (duration, relevance)
  * Feedback on **action verbs**, quantifiable achievements, bullet formatting
* Visualized via **Plotly/Altair charts** for skill frequency, experience durations, and resume section breakdowns

---

### 3. 🔍 Job Recommender

* Input via resume-derived skills or manual skill entry
* Uses:

  * **Keyword matching** (fuzzy/partial)
  * Optional **ML model** (e.g., TF-IDF + cosine similarity / recommendation classifier)
* With integration: fetches live jobs via APIs (e.g., Indeed or LinkedIn)
* Displays:

  * Top matches with title, company, short summary
  * Role fit percentage scores
  * Downloadable as CSV or JSON for personal tracking

---

### 4. 🎤 Interview Preparation Toolkit

* Loads resume-sourced key skills and target roles
* Generates 5–10 common questions per role using GPT/Gemini API or pre-defined mappings
* Provides:

  * Sample structured answers
  * Tips (e.g., use of STAR method, highlighting achievements)
* Option to simulate a Q\&A session with feedback on answer completeness and structure

---

### 5. 🧩 Skill Gap Analysis

* Compares your skills to requirements drawn from:

  * Job listings
  * Industry databases
* Highlights:

  * Skills you're missing
  * Undervalued strengths
* Suggests formatted resource lists:

  * LinkedIn Learning, Coursera, Udemy links
  * Community tutorials and free resources

---

### 6. 📊 Job Market Insights

* Scrapes or uses APIs to gather:

  * Average salary by location for roles
  * Job posting volume over time
  * Common qualification & skill requirements
* Presents:

  * Interactive bar/line charts
  * Filter options (e.g., by region, seniority level, industry)

---

### 7. ✅ Personalized Advice & Downloads

* In **each module**, generates tailored summaries and tips:

  * “Your resume is heavy on bullet points—consider adding metrics.”
  * “Introductory-level positions scoring 70% match, mid-level 45%.”
* Exportable artifacts:

  * Detailed **Resume Analysis Report**
  * **Interview Q\&A Summary** PDF
  * **Job Recommendation List** CSV
  * **Skill Gap Summary** with improvement roadmaps

---

### 8. 🔐 Session Persistence

* Uses Streamlit’s Session State to:

  * Retain uploaded files and analysis
  * Enable back-and-forth switching without losing input
* Foundation in place for future logged-in user profiles and dashboards

---

## 🛠️ Tech Stack Breakdown

| Component                | Technology/Library                  | Purpose                                              |
| ------------------------ | ----------------------------------- | ---------------------------------------------------- |
| **Front-end**            | Streamlit                           | UI framework                                         |
| **Backend (core logic)** | Python                              | Orchestration & data processing                      |
| **Resume Parsing**       | PyMuPDF, textract                   | Text extraction from uploaded docs                   |
| **NLP Analysis**         | spaCy, optionally NLTK              | Entity recognition, skill extraction, recommendation |
| **Visualizations**       | Plotly, Altair                      | Charts for skills, matching, market insights         |
| **Data & Analysis**      | Pandas, NumPy                       | Dataframes and processing                            |
| **Interview Questions**  | OpenAI / Gemini API (optional)      | Generate dynamic interview Q\&A prompts              |
| **Job Market Data**      | Scraping or APIs (LinkedIn/Indeed)  | Role trends, salary, listings                        |
| **Downloadable Reports** | Python PDF libraries or HTML2PDF    | Export functionality                                 |
| **Session State**        | Streamlit’s in-memory session state | Keeps app state consistent during user session       |

---

## 🔧 Project Architecture & Flow

1. **User input** (upload resume or skills list) →
2. **Resume Analyzer** ↔ **Skill Extraction** → visual + text feedback →
3. **Job Recommender** ↔ **Market Role Matching** → top jobs displayed →
4. **Interview Prep** (based on skills + roles) → questions + tips →
5. **Skill Gap Module** (checks missing competencies)
6. **Market Insights Fetcher** → salary & demand charts →
7. **Export** reporting pipeline → users can download insights

Internal components communicate via shared data structures (pandas DataFrames + dicts), enabling smooth transitions and chained analysis.

---

## 🚀 Roadmap & Future Enhancements

1. **User Accounts & Dashboard** – save history, revisit reports
2. **ML-Powered Resume Scoring** – trained model for ranking quality
3. **Multilingual resumes** – Spanish, Hindi, French support
4. **Live Job API Integration** – fetch up-to-date listings
5. **Real-time Chatbot support** – embedded GPT/Gemini conversational agent
6. **Recruiter Dashboard** – evaluate candidates and collect feedback

---

## 👥 Who It's For

* 🎓 Students & fresh graduates
* 💼 Professionals in mid-career looking to switch roles
* 🚀 Career climbers seeking structured guidance
* 👁️ Job seekers desiring actionable insights before applying/interviewing

---

## 🧩 Why Use CAREERCRAFT JOB.AI?

* **Everything in one place**: resume, jobs, interview, skill gaps, market analysis
* **Actionable insights**: visual + textual takeaways for each module
* **Personalized intelligence**: provides feedback tailored to your documents
* **Exportable assets**: support records, tracking, and future reference
* **Scalable foundation**: designed for API/ML integration and user personalization

---

## 🔧 Next Steps

* Embed **real-world screenshots or demo GIFs** to visually demonstrate features
* Add **actual job recommendations** and **live interview simulation videos**
* Create a short video walkthrough for public users
* Set up **GitHub contributors’ guidelines** to invite open source collaboration

* git clone https://github.com/abhishekkumar62000/CAREERCRAFT-JOB.AI.git
cd careercraft-job-ai


# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate


### 🔧 **Prerequisites**  
Make sure you have the following installed:  
- ✅ Python 3.8+ 🐍  
- ✅ pip 📦  
- ✅ Streamlit 🌐  
- ✅ Google Gemini API key (for AI-powered features) 🔑  

## 🔥 **How to Run This Project Locally?**  

### **1️⃣ Clone This Repo**
```bash
git clone https://github.com/abhishekkumar62000/CAREERCRAFT-JOB.AI.git
cd ai-resumexpert-analyst
<p align="center">
  <img src="https://yourimageurl.com/contribute.png" alt="Contribute" width="500">
</p>

---
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---


## ❤️ **Made with Passion by Abhishek Yadav & Open-Source Contributors!** 🚀✨


<h1 align="center">© LICENSE <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Symbols/Check%20Box%20With%20Check.webp" alt="Check Box With Check" width="25" height="25" /></h1>

<table align="center">
  <tr>
     <td>
       <p align="center"> <img src="https://github.com/malivinayak/malivinayak/blob/main/LICENSE-Logo/MIT.png?raw=true" width="80%"></img>
    </td>
    <td> 
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg"/> <br> 
This project is licensed under <a href="./LICENSE">MIT</a>. <img width=2300/>
    </td>
  </tr>
</table>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900">




 <hr>

<div align="center">
<a href="#"><img src="assets/githubgif.gif" width="150"></a>
	
### **Thanks for checking out my GitHub Profile!**  

 ## 💌 Sponser

  [![BuyMeACoffee](https://img.buymeacoffee.com/button-api/?text=Buymeacoffee&emoji=&slug=codingstella&button_colour=FFDD00&font_colour=000000&font_family=Comic&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/abhishekkumar62000)

## 👨‍💻 Developer Information
**Created by **Abhishek kumar** 
**📧 Email**: [abhiydv23096@gmail.com](mailto:abhiydv23096@gmail.com)  
**🔗 LinkedIn**: [Abhishek Kumar](https://www.linkedin.com/in/abhishek-kumar-70a69829a/)  
**🐙 GitHub Profile**: [@abhishekkumar62000](https://github.com/abhishekkumar62000)  
**📸 Developer Profile Image**:- <img src="![1722245359938 (1)-photoaidcom-cropped-removebg-preview-photoaidcom-cropped jpg](https://github.com/user-attachments/assets/31ddd1bd-ccd9-46a4-921b-139d381f6f01)" width="150" height="150" style="border-radius: 50%;" alt="Developer Photo">

![1722245359938 (1)-photoaidcom-cropped-removebg-preview-photoaidcom-cropped jpg](https://github.com/user-attachments/assets/31ddd1bd-ccd9-46a4-921b-139d381f6f01)

</div>  

---
