#!/usr/bin/env python3
"""
Test script to verify Celery task can access GOOGLE_API_KEY
This simulates what happens when a Celery worker runs the grading task
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment_checker_project.settings')
django.setup()

from core.tasks import grade_with_gemini

def test_celery_grading():
    """Test if the grading function works when called directly (simulating Celery)"""
    print("🧪 Testing Celery Grading Function")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key loaded: {api_key[:10]}...")
    
    # Test data
    teacher_answer = """
    Q1. What is 2 + 2?
    Answer: 4
    
    Q2. What is the capital of France?
    Answer: Paris
    """
    
    student_answer = """
    Q1. 2 + 2 = 4
    
    Q2. Paris
    """
    
    try:
        print("🚀 Testing grade_with_gemini function...")
        result = grade_with_gemini(teacher_answer, student_answer, 10)
        
        print("✅ Grading completed successfully!")
        print(f"Total marks: {result.get('total_marks_allocated', 'N/A')}")
        print(f"Total score: {result.get('total_score', 'N/A')}")
        print(f"Feedback: {result.get('overall_feedback', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in grading: {e}")
        return False

if __name__ == "__main__":
    success = test_celery_grading()
    
    if success:
        print("\n🎉 Celery grading test passed!")
        print("Your Celery workers should now be able to access the Gemini API.")
    else:
        print("\n❌ Celery grading test failed!")
        print("Please check your configuration.")
    
    print("\n" + "=" * 50)
    print("Test completed.")
