from django.contrib import admin
from .models import FitnessClass, Booking

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time', 'instructor', 'available_slots', 'total_slots')
    list_filter = ('name', 'date_time')
    search_fields = ('instructor',)
    ordering = ('-date_time',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'fitness_class', 'booking_date')
    list_filter = ('fitness_class', 'booking_date')
    search_fields = ('client_name', 'client_email')
    ordering = ('-booking_date',)