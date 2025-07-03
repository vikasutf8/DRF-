from rest_framework import serializers
from students.models import Student
from employees.models import Employee

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('student_id', 'name', 'branch')   
        # fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_id', 'employee_name', 'designation')
        # fields = '__all__'