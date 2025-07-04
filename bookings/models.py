from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class FitnessClass(models.Model):
    CLASS_TYPES = [
        ('YOGA', 'Yoga'),
        ('ZUMBA', 'Zumba'),
        ('HIIT', 'HIIT'),
        ('PILATES', 'Pilates'),
        ('CYCLE', 'Cycle'),
    ]
    
    name = models.CharField(max_length=50, choices=CLASS_TYPES)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_slots = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.date_time.strftime('%d %b %Y %H:%M')}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New instance
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Fitness Classes"
        ordering = ['date_time']
        indexes = [
            models.Index(fields=['date_time']),
        ]

class Booking(models.Model):
    fitness_class = models.ForeignKey(
        FitnessClass, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.client_name} - {self.fitness_class}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New booking
            if self.fitness_class.available_slots <= 0:
                logger.error(f"No available slots for class {self.fitness_class.id}")
                raise ValueError("Class is fully booked")
            
            # Check if user already booked this class
            if Booking.objects.filter(
                fitness_class=self.fitness_class,
                client_email=self.client_email,
                is_active=True
            ).exists():
                logger.error(f"Duplicate booking attempt by {self.client_email}")
                raise ValueError("You've already booked this class")
            
            self.fitness_class.available_slots -= 1
            self.fitness_class.save()
        
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('fitness_class', 'client_email')
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['client_email']),
        ]