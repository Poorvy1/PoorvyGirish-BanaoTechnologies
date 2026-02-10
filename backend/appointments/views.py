from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone
from .models import Availability, Booking
from users.models import User
import requests


@csrf_exempt
def add_availability(request):
    """
    Doctor creates availability slots
    """
    if request.method != 'POST':
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=400
        )

    if request.user.role != 'doctor':
        return JsonResponse(
            {"error": "Only doctors can add availability"},
            status=403
        )

    date = request.POST.get('date')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')

    if not all([date, start_time, end_time]):
        return JsonResponse(
            {"error": "All fields are required"},
            status=400
        )

    Availability.objects.create(
        doctor=request.user,
        date=date,
        start_time=start_time,
        end_time=end_time
    )

    return JsonResponse({"message": "Availability slot created"})


def list_available_slots(request):
    """
    Patient views all available slots
    """
    if request.user.role != 'patient':
        return JsonResponse(
            {"error": "Only patients can view slots"},
            status=403
        )

    slots = Availability.objects.filter(
        is_booked=False,
        date__gte=timezone.now().date()
    )

    data = []
    for slot in slots:
        data.append({
            "slot_id": slot.id,
            "doctor": slot.doctor.username,
            "date": slot.date,
            "start_time": slot.start_time,
            "end_time": slot.end_time
        })

    return JsonResponse({"available_slots": data})


@csrf_exempt
@transaction.atomic
def book_slot(request, slot_id):
    """
    Patient books an available slot
    """
    if request.method != 'POST':
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=400
        )

    if request.user.role != 'patient':
        return JsonResponse(
            {"error": "Only patients can book slots"},
            status=403
        )

    try:
        slot = Availability.objects.select_for_update().get(id=slot_id)
    except Availability.DoesNotExist:
        return JsonResponse(
            {"error": "Slot not found"},
            status=404
        )

    if slot.is_booked:
        return JsonResponse(
            {"error": "Slot already booked"},
            status=400
        )

    slot.is_booked = True
    slot.save()

    Booking.objects.create(
        patient=request.user,
        availability=slot
    )

    # Call serverless email service
    try:
        requests.post(
            "http://localhost:3000/send-email",
            json={
                "type": "BOOKING_CONFIRMATION",
                "email": request.user.email
            },
            timeout=5
        )
    except Exception:
        pass

    return JsonResponse({"message": "Appointment booked successfully"})
