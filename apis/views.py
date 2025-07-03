
from students.models import Student
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
"""
def studentViews(request):
    student =Student.objects.all()
    # print(student)#<QuerySet [<Student: test1>, <Student: test2>]>
    # convert queryset to json.  --drf is serializing the queryset to json
    tempstudent =list(student.values())
    print(tempstudent)
    return JsonResponse(tempstudent, safe=False)
    
"""
@api_view(['GET'])
def studentViews(request):
    if request.method == 'GET':
        student =Student.objects.all()
        studentSerializer = StudentSerializer(student, many=True)
        return Response(studentSerializer.data, status=status.HTTP_200_OK)