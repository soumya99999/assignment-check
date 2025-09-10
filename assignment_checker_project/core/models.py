from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    """Custom User model that extends Django's AbstractUser"""
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    regdno = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Classroom(models.Model):
    """Classroom model for teachers to create classrooms"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_classrooms')
    code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    students = models.ManyToManyField(User, related_name='joined_classrooms', blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        """Generate a unique 6-character code for the classroom"""
        while True:
            code = str(uuid.uuid4())[:6].upper()
            if not Classroom.objects.filter(code=code).exists():
                return code

    def __str__(self):
        return f"{self.name} ({self.code})"


class Assignment(models.Model):
    """Assignment model for teachers to create assignments"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    question_file = models.FileField(upload_to='questions/', null=True, blank=True)
    correct_answer_file = models.FileField(upload_to='answers/')
    total_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Submission(models.Model):
    """Submission model for students to submit assignments"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submission_file = models.FileField(upload_to='submissions/')
    submission_date = models.DateTimeField(default=timezone.now)
    score = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    grading_details = models.JSONField(null=True, blank=True)
    plagiarism_report = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username}'s submission for {self.assignment.title}"
