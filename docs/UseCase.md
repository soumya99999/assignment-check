# Use Case

This project is an Assignment Checker system designed for educational environments. It enables teachers to create classrooms and assignments, while students can join and submit their work. The system automatically grades submissions using advanced techniques like OCR for text extraction from PDFs, similarity checks for plagiarism detection, and AI-powered evaluation using models like Gemini.

## What it Achieves

- Automates the grading process, reducing manual effort for teachers.
- Provides instant feedback to students.
- Detects plagiarism to maintain academic integrity.
- Generates Excel reports for easy analysis.
- Supports file uploads and handles various formats.

## Comparison to Others

Unlike traditional Learning Management Systems (LMS) like Moodle or Canvas, which often require manual grading or basic auto-grading for multiple-choice questions, this system offers:

- Advanced AI-based grading for open-ended assignments.
- OCR integration for handwritten or scanned submissions.
- Plagiarism detection using semantic embeddings.
- Asynchronous processing with Celery for scalability.
- Integration with modern web technologies (Django REST API + Svelte frontend).

This makes it more suitable for subjects requiring subjective evaluation, such as essays, math problems, or creative assignments, where AI can assist in providing consistent and fair grading.
