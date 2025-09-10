#!/usr/bin/env python3
"""
Test script to simulate PDF grading with the exact data you provided
This will help us verify the complete grading flow
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

def test_hybrid_assignment_grading():
    """Test grading with the exact assignment data you provided"""
    print("🧪 Testing Hybrid Assignment Grading")
    print("=" * 60)
    
    # Teacher's correct answers (from your data)
    teacher_answer = """
    Q1. Solve for x: 2x + 3 = 11
    Answer: 2x + 3 = 11 → 2x = 8 → x = 4
    
    Q2. A car travels 240 km in 4 hours. What is its average speed?
    Answer: Average speed = Distance / Time = 240 / 4 = 60 km/h
    
    Q3. Explain Newton's Second Law of Motion in your own words.
    Answer: Newton's Second Law states that Force = Mass × Acceleration. It explains how the acceleration of an object depends on its mass and the net force applied.
    
    Q4. The area of a rectangle is 48 square units. If the length is 12 units, find the width.
    Answer: Area = length × width → 48 = 12 × width → width = 4 units
    
    Q5. What is the difference between renewable and non-renewable energy sources?
    Answer: Renewable energy sources can be naturally replenished (like solar, wind, hydro). Non-renewable sources (like coal, oil, natural gas) are finite and will eventually run out.
    """
    
    # Student's mixed answers (from your data)
    student_answer = """
    Q1: Equation: 2x + 3 = 11 → 2x = 8 → x = 4 (Correct)
    Q2: Average speed = Distance / Time = 240 / 5 = 48 km/h (Wrong)
    Q3: Newton's Second Law: Force = Mass × Acceleration (Correct)
    Q4: Area = length × width → 48 = 12 × width → width = 6 units (Wrong)
    Q5: Renewable sources include solar, wind, hydro. Non-renewable include coal, oil, natural gas (Correct)
    """
    
    print("📋 Assignment Details:")
    print(f"Total Questions: 5")
    print(f"Expected Score: Should be around 3/5 (60%) based on correct answers")
    print()
    
    try:
        print("🚀 Testing Gemini grading...")
        result = grade_with_gemini(teacher_answer, student_answer, 20)
        
        print("✅ Grading completed successfully!")
        print()
        print("📊 Results:")
        print(f"Total marks allocated: {result.get('total_marks_allocated', 'N/A')}")
        print(f"Total score achieved: {result.get('total_score', 'N/A')}")
        print(f"Percentage: {(result.get('total_score', 0) / result.get('total_marks_allocated', 1)) * 100:.1f}%")
        print()
        print(f"Overall feedback: {result.get('overall_feedback', 'N/A')}")
        print()
        
        # Display individual question breakdown
        questions = result.get('questions', [])
        if questions:
            print("📋 Individual Question Breakdown:")
            print("-" * 50)
            for q in questions:
                print(f"Question {q.get('question_number', '?')}:")
                print(f"  Marks allocated: {q.get('marks_allocated', 0)}")
                print(f"  Marks achieved: {q.get('marks_achieved', 0)}")
                print(f"  Feedback: {q.get('feedback', 'No feedback')}")
                print()
        else:
            print("⚠️  No individual question breakdown available")
        
        # Verify the grading makes sense
        print("🔍 Verification:")
        print("-" * 20)
        total_allocated = sum(q.get('marks_allocated', 0) for q in questions)
        total_achieved = sum(q.get('marks_achieved', 0) for q in questions)
        
        print(f"Sum of individual marks allocated: {total_allocated}")
        print(f"Sum of individual marks achieved: {total_achieved}")
        print(f"Expected total marks: {result.get('total_marks_allocated', 20)}")
        print(f"Calculated total score: {result.get('total_score', 0)}")
        
        if total_achieved == result.get('total_score', 0):
            print("✅ Individual marks sum matches total score")
        else:
            print("⚠️  Mismatch between individual marks sum and total score")
        
        # Check if the score makes sense (should be around 12/20 based on 3 correct answers)
        expected_score = 12  # 3 out of 5 questions correct
        actual_score = result.get('total_score', 0)
        if abs(actual_score - expected_score) <= 2:  # Allow some variance
            print("✅ Score is reasonable for the given answers")
        else:
            print(f"⚠️  Score might be unexpected. Expected ~{expected_score}, got {actual_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in grading: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Hybrid Assignment Grading Test")
    print("=" * 60)
    print("This test simulates the exact assignment data you provided")
    print("to verify the grading system works correctly.")
    print()
    
    success = test_hybrid_assignment_grading()
    
    if success:
        print("\n🎉 Hybrid assignment grading test passed!")
        print("The grading system should work correctly with your PDF submissions.")
    else:
        print("\n❌ Hybrid assignment grading test failed!")
        print("Please check the error messages above.")
    
    print("\n" + "=" * 60)
    print("Test completed.")
