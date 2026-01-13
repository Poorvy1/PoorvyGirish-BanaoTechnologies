from django.urls import path
from .views import add_availability, list_available_slots, book_slot

urlpatterns = [
    path('add-slot/', add_availability, name='add_availability'),
    path('available-slots/', list_available_slots, name='available_slots'),
    path('book/<int:slot_id>/', book_slot, name='book_slot'),
]
