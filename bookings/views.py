from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
import logging

logger = logging.getLogger(__name__)

class FitnessClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'instructor']
    
    def get_queryset(self):
        queryset = FitnessClass.objects.filter(date_time__gte=timezone.now())
        
        # Filter by class type if provided
        class_type = self.request.query_params.get('type')
        if class_type:
            queryset = queryset.filter(name__iexact=class_type)
        
        # Filter by instructor if provided
        instructor = self.request.query_params.get('instructor')
        if instructor:
            queryset = queryset.filter(instructor__icontains=instructor)
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date_time__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_time__date__lte=end_date)
        
        return queryset.order_by('date_time')


class BookClassView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info(f"New booking created: {serializer.data}")
            return Response(
                {
                    'success': True,
                    'message': 'Booking successful!',
                    'data': serializer.data
                }, 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        except Exception as e:
            logger.error(f"Booking failed: {str(e)}")
            return Response(
                {
                    'success': False,
                    'message': str(e)
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ClientBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        email = self.request.query_params.get('email')
        if not email:
            return Booking.objects.none()
        
        return Booking.objects.filter(
            client_email=email,
            fitness_class__date_time__gte=timezone.now(),
            is_active=True
        ).select_related('fitness_class').order_by('-booking_date')