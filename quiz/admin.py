from django.contrib import admin
from .models import Class, Subject, Quiz ,TeamMember

admin.site.register(Class)
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(TeamMember)