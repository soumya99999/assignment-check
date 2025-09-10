## Description

This is a Django REST API project for managing assignments in classrooms. It allows teachers to create classrooms, assignments, and automatically grade student submissions using OCR, similarity checks, and plagiarism detection. Students can join classrooms, submit assignments, and view their grades.
## Features

- User registration and authentication (JWT)
- Classroom creation and joining via codes
- Assignment creation with file uploads
- Automatic submission grading using Celery
- Plagiarism detection
- Excel report generation
- Frontend integration (Svelte)