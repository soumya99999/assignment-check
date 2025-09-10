"""URL configuration for assignment_checker_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core.views import AssignmentViewSet, SubmissionViewSet, ClassroomViewSet, register_view, LoginView, assignment_report, join_classroom, current_user_view

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'classrooms', ClassroomViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register', register_view, name='register'),
    path('api/login', LoginView.as_view(), name='login'),
    path('api/user', current_user_view, name='current_user'),
    path('api/join-classroom', join_classroom, name='join_classroom'),
    path('api/assignments/<int:assignment_id>/report/', assignment_report, name='assignment_report'),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
