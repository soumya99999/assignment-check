import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment_checker_project.settings')
django.setup()

from core.tasks import grade_with_gemini

# Test data - sample teacher and student answers
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

student_answer = """
Q1. 2x + 3 = 11
2x = 8
x = 4

Q2. Speed = 240 / 4 = 60 km/h

Q3. Force = mass * acceleration

Q4. 48 = 12 * width
width = 4

Q5. Renewable can be renewed, non-renewable cannot
"""

print("Testing Gemini 2.5 Flash grading integration...")
print("=" * 60)

try:
    # Test the Gemini grading function
    result = grade_with_gemini(teacher_answer, student_answer, 20)

    print("✅ Gemini grading completed successfully!")
    print(f"Total marks allocated: {result.get('total_marks_allocated', 'N/A')}")
    print(f"Total score achieved: {result.get('total_score', 'N/A')}")
    print(f"Overall feedback: {result.get('overall_feedback', 'N/A')}")
    print()

    # Display individual question breakdown
    questions = result.get('questions', [])
    if questions:
        print("📋 Individual Question Breakdown:")
        print("-" * 40)
        for q in questions:
            print(f"Question {q.get('question_number', '?')}:")
            print(f"  Marks allocated: {q.get('marks_allocated', 0)}")
            print(f"  Marks achieved: {q.get('marks_achieved', 0)}")
            print(f"  Feedback: {q.get('feedback', 'No feedback')}")
            print()
    else:
        print("⚠️  No individual question breakdown available")

    # Verify the grading meets requirements
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

except Exception as e:
    print(f"❌ Error testing Gemini grading: {e}")
    print("Please check your GEMINI_API_KEY environment variable")

print("\n" + "=" * 60)
print("Test completed.")
