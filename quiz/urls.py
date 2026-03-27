from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health, name='health'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path("class/<int:class_id>/", views.subjects, name="subjects"),
    path("subject/<int:subject_id>/", views.quizzes, name="quizzes"),
    path("quiz/<int:quiz_id>/take/", views.take_quiz, name="take_quiz"),
    path("quiz/<int:quiz_id>/submit/", views.submit_quiz, name="submit_quiz"),
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
    path("quiz/<int:quiz_id>/leaderboard/", views.quiz_leaderboard, name="quiz_leaderboard"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),
    path("about/", views.about, name="about"),
]