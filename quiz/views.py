from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import re
from .models import Class, Subject, Quiz

# Landing page
def home(request):
    return render(request, "quiz/index.html")


# Register
def register_view(request):

    if request.method == "POST":

        fullname = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")

        if not email:
            return JsonResponse({"error": "Email is required"})

        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            return JsonResponse({"error": "Only Gmail allowed"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = fullname
        user.save()

        return JsonResponse({"success": True})

    return render(request, "quiz/register.html")

# Login
def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        else:
            return render(request, "quiz/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "quiz/login.html")

# Logout
def logout_view(request):
    logout(request)
    return redirect("home")


# Dashboard
from .models import Class

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    classes = Class.objects.all()

    return render(request, "quiz/dashboard.html", {
        "classes": classes
    })




def subjects(request, class_id):

    class_obj = Class.objects.get(id=class_id)

    subjects = Subject.objects.filter(class_name=class_obj)

    return render(request, "quiz/subjects.html", {
        "class": class_obj,
        "subjects": subjects
    })


def quizzes(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id)

    quizzes = Quiz.objects.filter(subject=subject)

    for quiz in quizzes:

        try:
            data = quiz.questions_json   # ✅ already dict

            quiz.question_count = len(data.get("questions", []))
            quiz.duration_minutes = data.get("duration_minutes", 5)

        except Exception as e:
            print("JSON ERROR:", e)
            quiz.question_count = 0
            quiz.duration_minutes = 5

    return render(request, "quiz/quizzes.html", {
        "subject": subject,
        "quizzes": quizzes
    })

import json



def take_quiz(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    data = quiz.questions_json

    if isinstance(data, str):
        data = json.loads(data)

    questions = data.get("questions", [])
    duration = data.get("duration_minutes", 5)

    return render(request, "quiz/take-quiz.html", {
        "quiz": quiz,
        "questions": questions,
        "duration": duration
    })


import json
from django.http import JsonResponse


def submit_quiz(request, quiz_id):

    if request.method == "POST":

        quiz = get_object_or_404(Quiz, id=quiz_id)

        data = quiz.questions_json

        if isinstance(data, str):
            data = json.loads(data)

        questions = data.get("questions", [])

        user_answers = json.loads(request.body)

        correct = 0
        wrong = 0
        skipped = 0

        for i, q in enumerate(questions):

            user_ans = user_answers.get(str(i))

            if user_ans is None:
                skipped += 1

            elif int(user_ans) == q["rightAnswerIndex"]:
                correct += 1

            else:
                wrong += 1

        total = len(questions)

        score = round((correct / total) * 100) if total > 0 else 0

        return JsonResponse({
            "correct": correct,
            "wrong": wrong,
            "skipped": skipped,
            "score": score,
            "total": total
        })

def quiz_result(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    return render(request, "quiz/quiz-result.html", {
        "quiz": quiz,
        "correct_count": 0,
        "wrong_count": 0,
        "skipped_count": 0,
        "score": 0,
        "total_questions": 0,
        "result_items": [],
        "leaderboard": []
    })