from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .models import Classroom, Assignment, Submission, User
from .serializers import ClassroomSerializer, AssignmentSerializer, SubmissionSerializer, UserRegistrationSerializer, UserSerializer
from .permissions import IsTeacher, IsStudent, IsOwnerOrTeacher


class AssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Assignment instances"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, IsTeacher]
        return super().get_permissions()

    def get_queryset(self):
        # Teachers can see all assignments, students can only see assignments assigned to classrooms they joined
        user = self.request.user
        if user.role == 'teacher':
            return Assignment.objects.filter(teacher=user)
        else:  # student
            return Assignment.objects.filter(classroom__students=user)


class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Submission instances"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, IsStudent]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrTeacher]
        return super().get_permissions()

    def get_queryset(self):
        # Teachers can see all submissions for their assignments
        # Students can only see their own submissions
        user = self.request.user
        if user.role == 'teacher':
            return Submission.objects.filter(assignment__teacher=user)
        else:  # student
            return Submission.objects.filter(student=user)


class ClassroomViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Classroom instances"""
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, IsTeacher]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsTeacher]
        return super().get_permissions()

    def get_queryset(self):
        # Teachers can see their own classrooms, students can see classrooms they joined
        user = self.request.user
        if user.role == 'teacher':
            return Classroom.objects.filter(teacher=user)
        else:  # student
            return Classroom.objects.filter(students=user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """View for user registration"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """View for user login with JWT token"""
    pass


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsTeacher])
def assignment_report(request, assignment_id):
    """Generate Excel report for assignment submissions"""
    try:
        assignment = Assignment.objects.get(id=assignment_id, teacher=request.user)
        submissions = Submission.objects.filter(assignment=assignment).select_related('student')

        import pandas as pd
        from django.http import HttpResponse

        data = []
        for sub in submissions:
            # Convert timezone-aware datetime to naive for Excel compatibility
            submission_date_naive = sub.submission_date.replace(tzinfo=None) if sub.submission_date else None
            data.append({
                'Name': sub.student.get_full_name() or sub.student.username,
                'Regd No': sub.student.regdno or 'N/A',
                'Secured Mark': sub.score or 'Pending',
                'Total Mark': sub.assignment.total_marks,
            })

        df = pd.DataFrame(data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="assignment_{assignment_id}_report.xlsx"'
        df.to_excel(response, index=False)
        return response

    except Assignment.DoesNotExist:
        return Response({'error': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsStudent])
def join_classroom(request):
    """API for students to join a classroom using code"""
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Classroom code is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        classroom = Classroom.objects.get(code=code.upper())
        user = request.user

        if classroom.students.filter(id=user.id).exists():
            return Response({'message': 'Already joined this classroom'}, status=status.HTTP_200_OK)

        classroom.students.add(user)
        serializer = ClassroomSerializer(classroom, context={'request': request})
        return Response({
            'message': 'Successfully joined classroom',
            'classroom': serializer.data
        }, status=status.HTTP_200_OK)

    except Classroom.DoesNotExist:
        return Response({'error': 'Invalid classroom code'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user_view(request):
    """API for getting current user data"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
