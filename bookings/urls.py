from django.urls import path
from .views import FitnessClassListView, BookClassView, ClientBookingsView

urlpatterns = [
    path('classes/', FitnessClassListView.as_view(), name='class-list'),
    path('book/', BookClassView.as_view(), name='book-class'),
    path('bookings/', ClientBookingsView.as_view(), name='client-bookings'),
]