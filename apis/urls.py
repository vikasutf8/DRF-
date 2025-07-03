
from django.urls import path, include
from . import views

urlpatterns = [
    path('students/', views.studentViews),
    path('students/<str:student_id>', views.studentDetail),
]