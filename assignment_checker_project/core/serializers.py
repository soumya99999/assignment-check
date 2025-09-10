from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Classroom, Assignment, Submission


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'regdno']
        read_only_fields = ['id']


class ClassroomSerializer(serializers.ModelSerializer):
    """Serializer for the Classroom model"""
    teacher = UserSerializer(read_only=True)
    students = UserSerializer(many=True, read_only=True)
    student_count = serializers.SerializerMethodField()
    assignment_count = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'description', 'teacher', 'code', 'created_at', 'students', 'student_count', 'assignment_count']
        read_only_fields = ['id', 'code', 'created_at']

    def get_student_count(self, obj):
        return obj.students.count()

    def get_assignment_count(self, obj):
        return obj.assignments.count()

    def create(self, validated_data):
        # Set the teacher to the current user
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'regdno', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        if data.get('role') == 'student' and not data.get('regdno'):
            raise serializers.ValidationError({'regdno': 'Registration number is required for students.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for the Assignment model"""
    teacher = UserSerializer(read_only=True)
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    submitted_students_count = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'teacher', 'classroom', 'question_file', 'correct_answer_file', 'total_marks', 'created_at', 'submitted_students_count']
        read_only_fields = ['id', 'created_at']

    def get_submitted_students_count(self, obj):
        return obj.submissions.count()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.role == 'student':
            # Students should not see the correct_answer_file
            self.fields.pop('correct_answer_file', None)

    def create(self, validated_data):
        # Set the teacher to the current user
        validated_data['teacher'] = self.context['request'].user
        return super().create(validated_data)


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for the Submission model"""
    student = UserSerializer(read_only=True)
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())

    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'submission_file', 'submission_date', 'score', 'plagiarism_report']
        read_only_fields = ['id', 'submission_date', 'score', 'plagiarism_report']

    def create(self, validated_data):
        # Set the student to the current user
        validated_data['student'] = self.context['request'].user
        submission = super().create(validated_data)
        # Trigger grading task
        from .tasks import grade_submission
        grade_submission.delay(submission.id)
        return submission


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
