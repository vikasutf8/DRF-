
from students.models import Student
from employees.models import Employee
from blogs.models import Blog, Comment
from .serializers import StudentSerializer, EmployeeSerializer
from blogs.serializers import BlogSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import viewsets
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from employees.filter import EmployeeFilter

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
    

"""
class EmployeeView(APIView):
    def get(self, request):
        employee = Employee.objects.all()
        employeeSerializer = EmployeeSerializer(employee, many=True)
        return Response(employeeSerializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        employeeSerializer = EmployeeSerializer(data=request.data)
        if employeeSerializer.is_valid():
            employeeSerializer.save()
            return Response(employeeSerializer.data, status=status.HTTP_201_CREATED)
        return Response(employeeSerializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        """
""" 
class EmployeeDetail(APIView):
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            employeeSerializer = EmployeeSerializer(employee)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(employeeSerializer.data, status=status.HTTP_200_OK)
    def put(self, request, employee_id):
        employee = Employee.objects.get(employee_id=employee_id)
        employeeSerializer = EmployeeSerializer(employee, data=request.data)
        if employeeSerializer.is_valid():
            employeeSerializer.save()               
            return Response(employeeSerializer.data, status=status.HTTP_200_OK)
        return Response(employeeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, employee_id):
        employee = Employee.objects.get(employee_id=employee_id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    def patch(self, request, employee_id):
        employee = Employee.objects.get(employee_id=employee_id)
        employeeSerializer = EmployeeSerializer(employee, data=request.data)
        if employeeSerializer.is_valid():
            employeeSerializer.save()
            return Response(employeeSerializer.data, status=status.HTTP_200_OK)
        return Response(employeeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """
"""
# MIXINS
class EmployeeView(mixins.ListModelMixin, mixins.CreateModelMixin,  GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class EmployeeDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_id'

    def get(self,request, employee_id):
        return self.retrieve(request, employee_id=employee_id)
    def put(self, request, employee_id):
        return self.update(request, employee_id = employee_id)
    def delete(self, request, employee_id):
        return self.destroy(request, employee_id=employee_id)
    def patch(self, request, empployee_id):
        return self.partial_update(request, empployee_id=empployee_id)


        """
"""
# GENERIC VIEWS

# class EmployeeView(generics.ListAPIView, generics.CreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     lookup_field = 'employee_id'


class EmployeeView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'employee_id'
    """


# VIEWSETS
"""
class EmployeeViewset(viewsets.ViewSet):
    def list(self, request):
        employee = Employee.objects.all()
        employeeSerializer = EmployeeSerializer(employee, many=True)
        return Response(employeeSerializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        employeeSerializer = EmployeeSerializer(data=request.data)
        if employeeSerializer.is_valid():
            employeeSerializer.save()
            return Response(employeeSerializer.data, status=status.HTTP_201_CREATED)
        return Response(employeeSerializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    def retrieve(self, request, employee_id=None):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            employeeSerializer = EmployeeSerializer(employee)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(employeeSerializer.data, status=status.HTTP_200_OK)
    def update(self, request, employee_id=None):
        employee = Employee.objects.get(employee_id=employee_id)
        employeeSerializer = EmployeeSerializer(employee, data=request.data)
        if employeeSerializer.is_valid():
            employeeSerializer.save()               
            return Response(employeeSerializer.data, status=status.HTTP_200_OK)
        return Response(employeeSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, employee_id=None):
        employee = Employee.objects.get(employee_id=employee_id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

"""
class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_class = EmployeeFilter


class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # lookup_field = 'slug
    lookup_field = 'pk'