from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import requests

User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=400
        )

    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    role = request.POST.get('role')

    if not all([username, password, email, role]):
        return JsonResponse(
            {"error": "All fields are required"},
            status=400
        )

    if role not in ['doctor', 'patient']:
        return JsonResponse(
            {"error": "Invalid role"},
            status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"error": "Username already exists"},
            status=400
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        role=role
    )

    # Call serverless email service (NON-BLOCKING)
    try:
        requests.post(
            "http://localhost:3000/send-email",
            json={
                "type": "SIGNUP_WELCOME",
                "to_email": email   
            },
            timeout=5
        )
    except Exception:
        pass  # Email failure should not break signup

    return JsonResponse({
        "message": "Signup successful",
        "username": user.username,
        "role": user.role
    })

