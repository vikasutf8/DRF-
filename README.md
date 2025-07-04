## Django Rest frameworks :
#### class-based views :: using functions
- web browser endpooint. vs  api endPoints

- Django allways experting  dictanary object return  ;; nor queryset neither list
- for list -- safe is false
```
﻿def studentViews(request):
student =Student.objects.all()
# print(student)#<QuerySet [<Student: test1>, <Student: test2>]>
# convert queryset to json.  --drf is serializing the queryset to json
tempstudent =list(student.values())
print(tempstudent)
return JsonResponse(tempstudent, safe=False) 
```
MIXING :reusable code functionality :class-based views

1. listModelMixins. :list() : class employee(mixins, generic.GenericAPIView)
2. CreateModelMixins : create()
3. UpdateModelMixins : reterive()
4. RetriewModelMixins : update()
5. DestoryModelMixins : destory()
GENERIC 

1.  listCreateAPIView
2. ReteriveUpdateAPIView
3. ReteriveUpdateDestoryAPIView
VIEWSETS :: with this ROUTERS

viewsets.ViewSet() -- handle all --> SHOULD used basename

viewsets.ModelViewSet -- takes only queryset and serialize class and automatically provided both pk and non-pk based operation



PAGENATION:

PageNumberBLOG

```
REST_FRAMEWORK = {
'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
'PAGE_SIZE': 2
}
```
LIMITOFFEST 

/blogs/?limit=10&offset=0

CustomPagenation 

```
from rest_framework import status
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param='page-num'
    max_page_size = 1
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
```
DJANGO_FILTER

```
'django_filters',
```
Global filter 

```
'DEFAULT_FILTER_BACKENDS': 'django_filters.rest_framework.DjangoFilterBackend',
```
