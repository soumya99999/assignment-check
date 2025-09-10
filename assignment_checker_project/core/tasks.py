import os
import json
import fitz
import pytesseract
from PIL import Image
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from .models import Submission, Assignment
import google.generativeai as genai
from dotenv import load_dotenv

logger = get_task_logger(__name__)

# Load environment variables from .env file (important for Celery workers)
load_dotenv()

# Configure Gemini once (API key from .env or settings)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("GOOGLE_API_KEY environment variable is not set. Please set it in your .env file.")
    raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini integration")
genai.configure(api_key=api_key)

@shared_task
def grade_submission(submission_id):
    """Background task to grade a submission using Gemini 1.5 Flash"""
    # Ensure environment variables are loaded in the Celery worker process
    load_dotenv()
    
    # Reconfigure Gemini with the API key (in case it wasn't loaded at module level)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY not found in Celery worker process")
        raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini integration")
    
    # Reconfigure Gemini for this task
    genai.configure(api_key=api_key)
    logger.info(f"Gemini configured with API key: {api_key[:10]}...")
    
    submission = Submission.objects.get(id=submission_id)
    assignment = submission.assignment
    try:
        submission_text = extract_text_from_pdf(submission.submission_file.path)
        answer_text = extract_text_from_pdf(assignment.correct_answer_file.path)
        grading_result = grade_with_gemini(answer_text, submission_text, assignment.total_marks)

        submission.score = min(grading_result['total_score'], assignment.total_marks)
        submission.grading_details = json.dumps(grading_result)
        submission.status = 'completed'
        submission.save()

        logger.info(f"Grading completed for submission {submission_id}")
        logger.debug(f"Detailed breakdown: {grading_result}")
        return grading_result
    except Exception as e:
        logger.error(f"Error grading submission {submission_id}: {e}")
        submission.status = 'failed'
        submission.save()
        raise

def extract_text_from_pdf(file_path):
    """Extract text from PDF, handling typed and handwritten content"""
    if not os.path.exists(file_path):
        logger.error(f"PDF file not found: {file_path}")
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text + "\n"
            else:
                try:
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.rgb)
                    img = img.convert("L")
                    page_text = pytesseract.image_to_string(img, config='--psm 6')
                    text += page_text + "\n"
                except Exception as ocr_error:
                    logger.warning(f"OCR failed for page {page.number} in {file_path}: {ocr_error}")
                    continue
    return text.strip()

def grade_with_gemini(teacher_answer, student_answer, total_marks):
    """Grade assignment using Gemini 1.5 Flash with detailed question-wise analysis"""
    if not teacher_answer.strip() or not student_answer.strip():
        return {
            "questions": [],
            "total_marks_allocated": total_marks,
            "total_score": 0,
            "overall_feedback": "Error: Empty teacher or student answer",
            "error": "Empty input"
        }
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        You are an expert educator grading student assignments. Analyze carefully:

        TEACHER'S ANSWER KEY:
        {teacher_answer}

        STUDENT'S SUBMISSION:
        {student_answer}

        TOTAL MARKS AVAILABLE: {total_marks}

        Tasks:
        1. Identify each question
        2. Allocate marks per question so that sum = total_marks
        3. Grade each question with marks_achieved
        4. Provide feedback per question
        5. Give overall feedback

        Respond ONLY in JSON:
        {{
            "questions": [
                {{
                    "question_number": 1,
                    "question_text": "extracted question text",
                    "marks_allocated": 5,
                    "marks_achieved": 4,
                    "feedback": "feedback here"
                }}
            ],
            "total_marks_allocated": {total_marks},
            "total_score": <sum of achieved marks>,
            "overall_feedback": "summary feedback"
        }}
        """

        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Remove markdown fences if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        result = json.loads(response_text)
        result["total_score"] = sum(q.get("marks_achieved", 0) for q in result.get("questions", []))
        result["total_marks_allocated"] = total_marks
        return result

    except Exception as e:
        logger.error(f"Error in Gemini grading: {e}")
        return {
            "questions": [],
            "total_marks_allocated": total_marks,
            "total_score": 0,
            "overall_feedback": f"Error in grading: {str(e)}",
            "error": str(e)
        }
