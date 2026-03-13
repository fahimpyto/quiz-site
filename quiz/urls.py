from django.urls import path
from . import views



urlpatterns = [

    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Class → Subjects
    path("class/<int:class_id>/", views.subjects, name="subjects"),

    # Subject → Quizzes
    path("subject/<int:subject_id>/", views.quizzes, name="quizzes"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
    path("quiz/<int:quiz_id>/leaderboard/", views.quiz_leaderboard, name="quiz_leaderboard"),


]