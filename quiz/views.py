from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
import re
def home(request):
    return render(request, 'quiz/base.html')


def register_view(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return JsonResponse({"error":"Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error":"Username already exists"})

        User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=fullname
        )

        return JsonResponse({"success":True})

    return render(request,"quiz/register.html")


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")

        # gmail check
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            return JsonResponse({"error":"Only Gmail allowed"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error":"Username already exists"})

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error":"Email already exists"})