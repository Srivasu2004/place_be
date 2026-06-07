from fastapi import FastAPI, UploadFile, File
import pdfplumber

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from langchain.tools import tool

# =========================
# APP INIT
# =========================
app = FastAPI(title="AI Resume Analyzer")

# Simple in-memory cache
resume_cache = {}

# =========================
# PDF READER
# =========================
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# =========================
# CORE AI FUNCTIONS
# =========================
def resume_reader(resume_text: str):
    return resume_text[:3000]


def job_matcher(resume: str, job_description: str):
    docs = [resume, job_description]

    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(docs)

    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(float(score * 100), 2)


def ats_score(resume: str, keywords: str):
    resume_words = set(resume.lower().split())
    keyword_list = keywords.lower().split()

    match = sum(1 for k in keyword_list if k in resume_words)
    score = (match / len(keyword_list)) * 100 if keyword_list else 0

    return round(score, 2)


# =========================
# LANGCHAIN TOOLS (OPTIONAL)
# =========================
@tool
def read_resume(text: str):
    """Extract and summarize resume text"""
    return resume_reader(text)


@tool
def match_job(resume: str, job_description: str):
    """Match resume with job description"""
    return job_matcher(resume, job_description)


@tool
def ats_calculator(resume: str, keywords: str):
    """Calculate ATS score based on keywords"""
    return ats_score(resume, keywords)


tools = [read_resume, match_job, ats_calculator]


# =========================
# API ROUTES
# =========================

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)
    resume_cache["resume"] = text

    return {
        "message": "Resume uploaded successfully",
        "length": len(text)
    }


@app.post("/job-match")
async def job_match(job_description: str):
    resume = resume_cache.get("resume", "")

    if not resume:
        return {"error": "No resume uploaded"}

    score = job_matcher(resume, job_description)

    return {
        "job_match_score": score
    }


@app.post("/ats-score")
async def ats_score_api(keywords: str):
    resume = resume_cache.get("resume", "")

    if not resume:
        return {"error": "No resume uploaded"}

    score = ats_score(resume, keywords)

    return {
        "ats_score": score
    }
