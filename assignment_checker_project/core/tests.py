import os
import django
from dotenv import load_dotenv
from django.test import TestCase
from django.core.files import File
from .models import User, Classroom, Assignment, Submission
from .tasks import (
    is_math_assignment,
    evaluate_stepwise_math,
    partial_credit_numeric,
    parse_steps,
    grade_math_assignment,
    grade_with_gemini
)

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment_checker_project.settings')
django.setup()


class GradingTests(TestCase):
    """Test cases for the enhanced grading functionality"""

    def test_is_math_assignment(self):
        """Test math assignment detection"""
        # Math assignment
        teacher_math = "Solve for x: 2x + 3 = 7\nStep 1: 2x = 4\nStep 2: x = 2"
        student_math = "2x + 3 = 7\n2x = 4\nx = 2"
        self.assertTrue(is_math_assignment(teacher_math, student_math))

        # Non-math assignment
        teacher_text = "Explain the water cycle in detail."
        student_text = "The water cycle involves evaporation, condensation, and precipitation."
        self.assertFalse(is_math_assignment(teacher_text, student_text))

    def test_parse_steps(self):
        """Test step parsing from text"""
        text = "1. 2x = 11 - 3\n2. 2x = 8\n3. x = 4"
        steps = parse_steps(text)
        self.assertEqual(len(steps), 3)
        self.assertIn("2x = 11 - 3", steps[0])

    def test_evaluate_stepwise_math(self):
        """Test stepwise math evaluation"""
        teacher_steps = ["2x = 11 - 3", "2x = 8", "x = 4"]
        student_steps = ["2x = 11 - 3", "2x = 8", "x = 4"]  # Correct
        scores = evaluate_stepwise_math(teacher_steps, student_steps)
        self.assertAlmostEqual(scores["step_1"], 33.33, places=2)  # 100/3 ≈ 33.33
        self.assertAlmostEqual(scores["step_2"], 33.33, places=2)
        self.assertAlmostEqual(scores["step_3"], 33.33, places=2)

    def test_partial_credit_numeric(self):
        """Test partial credit for numeric answers"""
        teacher = "The answer is 100"
        student_correct = "The answer is 100"
        student_close = "The answer is 95"  # 5% error
        student_wrong = "The answer is 50"  # 50% error

        score_correct = partial_credit_numeric(teacher, student_correct, 100)
        score_close = partial_credit_numeric(teacher, student_close, 100)
        score_wrong = partial_credit_numeric(teacher, student_wrong, 100)

        self.assertEqual(score_correct, 100.0)
        self.assertGreater(score_close, score_wrong)
        self.assertLess(score_close, 100.0)

    def test_grade_math_assignment(self):
        """Test complete math assignment grading"""
        teacher_answer = "1. 2x + 3 = 7\n2. 2x = 4\n3. x = 2"
        student_answer = "2x + 3 = 7\n2x = 4\nx = 2"

        score = grade_math_assignment(student_answer, teacher_answer, 100)
        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)

    def test_grade_with_gemini_basic(self):
        """Test basic Gemini grading functionality"""
        teacher_answer = """
        Q1. Solve for x: 2x + 3 = 11
        Answer: 2x + 3 = 11 → 2x = 8 → x = 4

        Q2. A car travels 240 km in 4 hours. What is its average speed?
        Answer: Average speed = Distance / Time = 240 / 4 = 60 km/h
        """

        student_answer = """
        Q1. 2x + 3 = 11
        2x = 8
        x = 4

        Q2. Speed = 240 / 4 = 60 km/h
        """

        result = grade_with_gemini(teacher_answer, student_answer, 20)

        # Check that result has expected structure
        self.assertIn('questions', result)
        self.assertIn('total_marks_allocated', result)
        self.assertIn('total_score', result)
        self.assertIn('overall_feedback', result)

        # Check that total marks is correct
        self.assertEqual(result['total_marks_allocated'], 20)

        # Check that score is reasonable (should be high for correct answers)
        self.assertGreaterEqual(result['total_score'], 0)
        self.assertLessEqual(result['total_score'], 20)

    def test_grade_with_gemini_empty_input(self):
        """Test Gemini grading with empty inputs"""
        result = grade_with_gemini("", "Some answer", 10)
        self.assertEqual(result['total_score'], 0)
        self.assertIn('error', result)

        result = grade_with_gemini("Some answer", "", 10)
        self.assertEqual(result['total_score'], 0)
        self.assertIn('error', result)

    def test_grade_with_gemini_mixed_answers(self):
        """Test Gemini grading with mixed correct/incorrect answers"""
        teacher_answer = """
        Q1. Solve for x: 2x + 3 = 11
        Answer: 2x + 3 = 11 → 2x = 8 → x = 4

        Q2. A car travels 240 km in 4 hours. What is its average speed?
        Answer: Average speed = Distance / Time = 240 / 4 = 60 km/h

        Q3. Explain Newton's Second Law of Motion.
        Answer: Force = Mass × Acceleration

        Q4. Area of rectangle: length=12, width=?
        Answer: Area = 12 × width = 48 → width = 4

        Q5. Difference between renewable and non-renewable energy?
        Answer: Renewable can be replenished, non-renewable cannot.
        """

        student_answer = """
        Q1: Equation: 2x + 3 = 11 → 2x = 8 → x = 4 (Correct)
        Q2: Average speed = Distance / Time = 240 / 5 = 48 km/h (Wrong)
        Q3: Newton's Second Law: Force = Mass × Acceleration (Correct)
        Q4: Area = length × width → 48 = 12 × width → width = 6 units (Wrong)
        Q5: Renewable sources include solar, wind, hydro. Non-renewable include coal, oil, natural gas (Correct)
        """

        result = grade_with_gemini(teacher_answer, student_answer, 20)

        # Check structure
        self.assertIn('questions', result)
        self.assertEqual(result['total_marks_allocated'], 20)

        # Check that questions are parsed
        questions = result.get('questions', [])
        self.assertGreater(len(questions), 0)

        # Check that individual marks sum to total
        total_achieved = sum(q.get('marks_achieved', 0) for q in questions)
        self.assertEqual(result['total_score'], total_achieved)


if __name__ == '__main__':
    import unittest
    unittest.main()
