from django.http import HttpResponse 
from django.shortcuts import render

# Create your views here.

def students(request):
    student =[
        {'id': 1, 'name': "Vikas", 'age': 20},
        {'id': 2, 'name': "Arya", 'age': 21},
        {'id': 3, 'name': "Rahul", 'age': 22},
        {'id': 4, 'name': "Ravi", 'age': 23},
        {'id': 5, 'name': "Raj", 'age': 24},
    ]
    return HttpResponse(student)