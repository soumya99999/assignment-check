# End-to-End API Endpoints for Assignment Checker

This document outlines the complete API flow for testing the assignment checker system from beginning to end.

## Authentication
All API endpoints except registration and login require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## 1. User Registration

### Register Teacher
- **Method**: POST
- **URL**: `/api/register`
- **Body**:
```json
{
  "username": "teacher1",
  "email": "teacher@example.com",
  "password": "password123",
  "role": "teacher",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Register Student
- **Method**: POST
- **URL**: `/api/register`
- **Body**:
```json
{
  "username": "student1",
  "email": "student@example.com",
  "password": "password123",
  "role": "student",
  "first_name": "Jane",
  "last_name": "Smith",
  "regdno": "REG12345"
}
```
- **Note**: `regdno` is required for students.

## 2. User Login

### Login (Teacher/Student)
- **Method**: POST
- **URL**: `/api/login`
- **Body**:
```json
{
  "username": "teacher1",
  "password": "password123"
}
```
- **Response**: Returns JWT access and refresh tokens

## 3. Classroom Management

### Create Classroom (Teacher)
- **Method**: POST
- **URL**: `/api/classrooms/`
- **Headers**: Authorization: Bearer <teacher_token>
- **Body**:
```json
{
  "name": "Mathematics 101",
  "description": "Introduction to Algebra"
}
```
- **Response**: Classroom object with generated code (e.g., "ABC123")

### Join Classroom (Student)
- **Method**: POST
- **URL**: `/api/join-classroom`
- **Headers**: Authorization: Bearer <student_token>
- **Body**:
```json
{
  "code": "ABC123"
}
```

## 4. Assignment Management

### Create Assignment (Teacher)
- **Method**: POST
- **URL**: `/api/assignments/`
- **Headers**: Authorization: Bearer <teacher_token>
- **Body**: (multipart/form-data)
```
title: "Algebra Homework 1"
description: "Solve the following equations"
classroom: 1
total_marks: 100
question_file: <upload_file> (optional)
correct_answer_file: <upload_file>
```

### List Assignments (Student)
- **Method**: GET
- **URL**: `/api/assignments/`
- **Headers**: Authorization: Bearer <student_token>
- **Response**: List of assignments in joined classrooms

## 5. Submission Management

### Submit Assignment (Student)
- **Method**: POST
- **URL**: `/api/submissions/`
- **Headers**: Authorization: Bearer <student_token>
- **Body**: (multipart/form-data)
```
assignment: 1
submission_file: <upload_file>
```
- **Note**: This triggers automatic grading via Celery task

### List Submissions (Teacher)
- **Method**: GET
- **URL**: `/api/submissions/`
- **Headers**: Authorization: Bearer <teacher_token>
- **Response**: List of submissions for teacher's assignments

### List Submissions (Student)
- **Method**: GET
- **URL**: `/api/submissions/`
- **Headers**: Authorization: Bearer <student_token>
- **Response**: List of student's own submissions

## 6. Reporting

### Generate Assignment Report (Teacher)
- **Method**: GET
- **URL**: `/api/assignments/{assignment_id}/report/`
- **Headers**: Authorization: Bearer <teacher_token>
- **Response**: Excel file download with submission details including:
  - Name
  - Regd No
  - Secured Mark
  - Total Mark

## Complete End-to-End Test Flow

1. Register teacher account
2. Login as teacher
3. Create classroom
4. Register student account
5. Login as student
6. Student joins classroom using code
7. Teacher creates assignment with question and answer files
8. Student submits assignment file
9. System automatically grades submission (OCR, similarity check, plagiarism detection)
10. Teacher views graded submissions
11. Teacher generates Excel report

## Notes
- File uploads require multipart/form-data
- Automatic grading happens asynchronously via Celery
- Plagiarism check compares against other submissions in the same assignment
- Reports include student names, registration numbers, secured marks, and total marks

