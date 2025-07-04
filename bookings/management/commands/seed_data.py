from django.core.management.base import BaseCommand
from bookings.models import FitnessClass
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Seed the database with initial fitness class data'
    
    def handle(self, *args, **options):
        classes = [
            {
                'name': 'YOGA',
                'date_time': timezone.now() + timedelta(days=1, hours=10),
                'instructor': 'Alice Johnson',
                'total_slots': 15,
            },
            {
                'name': 'ZUMBA',
                'date_time': timezone.now() + timedelta(days=2, hours=18),
                'instructor': 'Bob Smith',
                'total_slots': 20,
            },
            {
                'name': 'HIIT',
                'date_time': timezone.now() + timedelta(days=3, hours=7),
                'instructor': 'Charlie Brown',
                'total_slots': 10,
            },
            {
                'name': 'PILATES',
                'date_time': timezone.now() + timedelta(days=4, hours=16),
                'instructor': 'Diana Prince',
                'total_slots': 12,
            },
            {
                'name': 'CYCLE',
                'date_time': timezone.now() + timedelta(days=5, hours=6),
                'instructor': 'Ethan Hunt',
                'total_slots': 8,
            },
        ]
        
        for class_data in classes:
            FitnessClass.objects.create(**class_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded fitness classes'))