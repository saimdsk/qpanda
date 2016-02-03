from django.contrib import admin

from .models import Question, PollChoice

admin.site.register(Question)
admin.site.register(PollChoice)
