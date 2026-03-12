from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
import re


# Landing page
def home(request):
    return render(request, "quiz/index.html")


# Register page
def register_view(request):

    if request.method == "POST":

        fullname = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # email empty check
        if not email:
            return JsonResponse({"error": "Email is required"})

        # gmail validation
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            return JsonResponse({"error": "Only Gmail allowed"})

        # username exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"})

        # email exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"})

        # create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fullname
        )

        return JsonResponse({"success": True})

    return render(request, "quiz/register.html")


# Login page
def login_view(request):
    return render(request, "quiz/login.html")


# Logout placeholder
def logout_view(request):
    return render(request, "quiz/index.html")