from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_name} - {self.name}"


class Quiz(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    questions_json = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    score = models.IntegerField()
    total = models.IntegerField()

    attempt_number = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)


from django.db import models

class TeamMember(models.Model):

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    details = models.TextField()

    image = models.ImageField(upload_to="team/")

    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name