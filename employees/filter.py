
from django_filters import rest_framework as filters
from .models import Employee

class EmployeeFilter(filters.FilterSet):
    designation = filters.CharFilter(field_name='designation', lookup_expr='iexact')
    employee_name = filters.CharFilter(field_name='employee_name', lookup_expr='icontains')
    # employee_id= filters.RangeFilter(field_name='employee_id', lookup_expr='range')
    id_min =filters.CharFilter(method='filter_id_range', label='From Min ID')
    id_max =filters.CharFilter(method='filter_id_range', label='To Max ID')

    class Meta:
        model = Employee
        fields = ['designation', 'employee_name', 'id_min', 'id_max']



def filter_id_range(self, queryset, name, value):
    if name == 'id_min':
        queryset = queryset.filter(employee_id__gte=value)
    elif name == 'id_max':
        queryset = queryset.filter(employee_id__lte=value)
    return queryset