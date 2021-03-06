"""QuestionPanda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from qpanda import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^question/', views.question, name='question'),
    url(r'^register/', views.register, name='register'),
    url(r'^(?P<question_id>[a-zA-Z0-9]+)/moreanswers', views.ajax_more_answers, name='ajax_more_answers'),
    url(r'^(?P<question_id>[a-zA-Z0-9]+)/answer/', views.answer_question, name='answerquestion'),
    url(r'^(?P<question_id>[a-zA-Z0-9]+)', views.asked_question, name='asked_question'),
    url(r'^$', views.ask_question, name='ask_question'),  # forward everything to qpanda.
]
