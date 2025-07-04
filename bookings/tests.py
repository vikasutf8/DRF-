from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from .models import FitnessClass, Booking
from datetime import timedelta
import json

class FitnessClassAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.yoga_class = FitnessClass.objects.create(
            name='YOGA',
            date_time=timezone.now() + timedelta(days=1),
            instructor='John Doe',
            total_slots=10,
        )
        self.zumba_class = FitnessClass.objects.create(
            name='ZUMBA',
            date_time=timezone.now() + timedelta(days=2),
            instructor='Jane Smith',
            total_slots=5,
        )
    
    def test_get_classes(self):
        response = self.client.get('/api/classes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_filter_classes_by_type(self):
        response = self.client.get('/api/classes/?name=YOGA')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'YOGA')
    
    def test_filter_classes_by_date(self):
        today = timezone.now().date()
        tomorrow = (timezone.now() + timedelta(days=1)).date()
        
        response = self.client.get(f'/api/classes/?start_date={tomorrow}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.class1 = FitnessClass.objects.create(
            name='HIIT',
            date_time=timezone.now() + timedelta(days=1),
            instructor='Mike Johnson',
            total_slots=3,
        )
    
    def test_create_booking(self):
        data = {
            'fitness_class': self.class1.id,
            'client_name': 'Test User',
            'client_email': 'test@example.com'
        }
        response = self.client.post(
            '/api/book/', 
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(Booking.objects.count(), 1)
        
        # Check available slots decreased
        self.class1.refresh_from_db()
        self.assertEqual(self.class1.available_slots, 2)
    
    def test_duplicate_booking(self):
        Booking.objects.create(
            fitness_class=self.class1,
            client_name='Test User',
            client_email='test@example.com'
        )
        
        data = [
            'fitness_class': self.class1.id,
            'client_name': 'Test User',
            client_email': 'test@example.com'
        ]
        response = self.client.post(
            '/api/book/', 
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You\'ve already booked this class', response.data['message'])
    
    def test_get_client_bookings(self):
        # Create a booking
        Booking.objects.create(
            fitness_class=self.class1,
            client_name='Test User',
            client_email='test@example.com'
        )
        
        response = self.client.get('/api/bookings/?email=test@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['client_email'], 'test@example.com')

class EdgeCaseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.full_class = FitnessClass.objects.create(
            name='PILATES',
            date_time=timezone.now() + timedelta(days=1),
            instructor='Sarah Connor',
            total_slots=1,
            available_slots=0
        )
        self.past_class = FitnessClass.objects.create(
            name='YOGA',
            date_time=timezone.now() - timedelta(days=1),
            instructor='Old Instructor',
            total_slots=10,
        )
    
    def test_book_full_class(self):
        data = {
            'fitness_class': self.full_class.id,
            'client_name': 'Test User',
            'client_email': 'test@example.com'
        }
        response = self.client.post(
            '/api/book/', 
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Class is fully booked', response.data['message'])
    
    def test_book_past_class(self):
        data = {
            'fitness_class': self.past_class.id,
            'client_name': 'Test User',
            'client_email': 'test@example.com'
        }
        response = self.client.post(
            '/api/book/', 
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot book a class that has already occurred', response.data['message'])