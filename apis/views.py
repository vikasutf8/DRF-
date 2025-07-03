from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.

def studentViews(request):
    student ={'id': 1, 'name': "Vikas", 'age': 20}
        
    
    return JsonResponse(student)