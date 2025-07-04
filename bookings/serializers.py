from rest_framework import serializers
from .models import FitnessClass, Booking
from django.utils import timezone
from datetime import timedelta

class FitnessClassSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()
    
    class Meta:
        model = FitnessClass
        fields = [
            'id', 'name', 'formatted_time', 'instructor', 
            'total_slots', 'available_slots', 'status'
        ]
    
    def get_status(self, obj):
        if obj.available_slots <= 0:
            return "Fully Booked"
        elif obj.date_time - timezone.now() < timedelta(hours=24):
            return "Starting Soon"
        return "Available"
    
    def get_formatted_time(self, obj):
        return obj.date_time.astimezone().strftime('%d %b %Y, %H:%M')

class BookingSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fitness_class.name', read_only=True)
    class_time = serializers.DateTimeField(
        source='fitness_class.date_time', 
        read_only=True,
        format='%d %b %Y, %H:%M'
    )
    instructor = serializers.CharField(source='fitness_class.instructor', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'fitness_class', 'class_name', 'class_time', 
            'instructor', 'client_name', 'client_email', 'booking_date'
        ]
        extra_kwargs = {
            'fitness_class': {'write_only': True}
        }
    
    def validate_fitness_class(self, value):
        if value.date_time < timezone.now():
            raise serializers.ValidationError("Cannot book a class that has already occurred")
        return value