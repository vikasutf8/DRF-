
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
@api_view(['GET','POST'])
def studentViews(request):
    if request.method == 'GET':
        student =Student.objects.all()
        studentSerializer = StudentSerializer(student, many=True)
        return Response(studentSerializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        studentSerializer = StudentSerializer(data=request.data)
        if studentSerializer.is_valid():
            studentSerializer.save()
            return Response(studentSerializer.data, status=status.HTTP_201_CREATED)
        return Response(studentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def studentDetail(request, student_id):
    try:
        student = Student.objects.get(student_id=student_id)
        studentSerializer = StudentSerializer(student)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(studentSerializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        studentSerializer = StudentSerializer(student, data=request.data)
        if studentSerializer.is_valid():
            studentSerializer.save()
            return Response(studentSerializer.data, status=status.HTTP_200_OK)
        return Response(studentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    elif request.method == 'PATCH':
        studentSerializer = StudentSerializer(student, data=request.data)
        if studentSerializer.is_valid():
            studentSerializer.save()
            return Response(studentSerializer.data, status=status.HTTP_200_OK)
        return Response(studentSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    