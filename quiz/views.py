from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import re
import json

from .models import Class, Subject, Quiz, QuizAttempt


# Landing page
def home(request):

    # Logged in user → dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

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

    if request.user.is_authenticated:
        return redirect("dashboard")

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
@login_required
def dashboard(request):

    classes = Class.objects.all()

    return render(request, "quiz/dashboard.html", {
        "classes": classes
    })


# Subjects
@login_required
def subjects(request, class_id):

    class_obj = get_object_or_404(Class, id=class_id)

    subjects = Subject.objects.filter(class_name=class_obj)

    return render(request, "quiz/subjects.html", {
        "class": class_obj,
        "subjects": subjects
    })


# Quizzes
@login_required
def quizzes(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id)

    quizzes = Quiz.objects.filter(subject=subject)

    for quiz in quizzes:

        try:
            data = quiz.questions_json

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


# Take quiz
@login_required
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


# Submit quiz
@login_required
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

        result_items = []

        for i, q in enumerate(questions):

            user_ans = user_answers.get(str(i + 1))
            correct_index = q["rightAnswerIndex"]

            options = []

            for j, opt in enumerate(q["options"]):

                options.append({
                    "letter": chr(65 + j),
                    "text": opt,
                    "is_correct": j == correct_index,
                    "is_user_choice": user_ans is not None and int(user_ans) == j
                })

            if user_ans is None:
                skipped += 1
                is_correct = False
                is_skipped = True

            elif int(user_ans) == correct_index:
                correct += 1
                is_correct = True
                is_skipped = False

            else:
                wrong += 1
                is_correct = False
                is_skipped = False

            result_items.append({
                "question_text": q["text"],
                "options": options,
                "is_correct": is_correct,
                "is_skipped": is_skipped
            })

        total = len(questions)
        score = correct

        attempt_count = QuizAttempt.objects.filter(
            user=request.user,
            quiz=quiz
        ).count() + 1

        QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            total=total,
            attempt_number=attempt_count
        )

        request.session["quiz_result"] = {
            "correct": correct,
            "wrong": wrong,
            "skipped": skipped,
            "score": score,
            "total": total,
            "result_items": result_items
        }

        return JsonResponse({
            "redirect": f"/quiz/{quiz_id}/result/"
        })


# Result page
@login_required
def quiz_result(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    result = request.session.get("quiz_result", {
        "correct": 0,
        "wrong": 0,
        "skipped": 0,
        "score": 0,
        "total": 0,
        "result_items": []
    })

    leaderboard = QuizAttempt.objects.filter(
        quiz=quiz
    ).order_by("-score", "created_at")[:3]

    return render(request, "quiz/quiz-result.html", {
        "quiz": quiz,
        "correct_count": result["correct"],
        "wrong_count": result["wrong"],
        "skipped_count": result["skipped"],
        "score": result["score"],
        "total_questions": result["total"],
        "result_items": result["result_items"],
        "leaderboard": leaderboard
    })


# Leaderboard page
@login_required
def quiz_leaderboard(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)

    leaderboard = QuizAttempt.objects.filter(
        quiz=quiz
    ).order_by("-score", "created_at")

    return render(request, "quiz/quiz_leaderboard.html", {
        "quiz": quiz,
        "leaderboard": leaderboard
    })

from .models import TeamMember

def about(request):

    members = TeamMember.objects.all()

    return render(request, "quiz/about.html", {
        "members": members
    })


from django.http import HttpResponse

def health(request):
    return HttpResponse("Server running")