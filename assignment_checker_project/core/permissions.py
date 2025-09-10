from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    """Custom permission to only allow teachers to create assignments"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'


class IsStudent(permissions.BasePermission):
    """Custom permission to only allow students to create submissions"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'student'


class IsOwnerOrTeacher(permissions.BasePermission):
    """Custom permission to only allow owners or teachers to edit objects"""

    def has_object_permission(self, request, view, obj):
        # Teachers can edit any object
        if request.user.role == 'teacher':
            return True
        # Students can only edit their own objects
        return obj.student == request.user
