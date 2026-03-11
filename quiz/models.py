from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question = models.TextField()

    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct = models.CharField(max_length=200)

    def __str__(self):
        return self.question
