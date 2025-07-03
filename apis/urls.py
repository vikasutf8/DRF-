
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('employees', views.EmployeeViewset, basename='employees')
router.register('employees', views.EmployeeViewset )


urlpatterns = [
    path('students/', views.studentViews),
    path('students/<str:student_id>', views.studentDetail),

    # path('employees/', views.EmployeeView.as_view()),
    # path('employees/<str:employee_id>', views.EmployeeDetail.as_view()),

    path('',include(router.urls)),

]