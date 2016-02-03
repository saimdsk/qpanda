
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User

from .forms import QuestionForm
from .models import Question

# Create your views here.

def index(request):
    return render(request, 'qpanda/index.html')
    # return HttpResponse("WELCOME TO QUESTIONPANDA!")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    return HttpResponse("You're looking at the results of question %s." % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def askquestion(request):
    context = {'test':True, 'test2':'WORKING!'}
    form = QuestionForm()
    context['form'] = form
    return render(request, 'qpanda/askquestion.html', context)
    # return HttpResponse("Just checking to see if the templates are working correctly. If this displays, they are.")

def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['question_text']

        dt = timezone.now()
        yaseen = User.objects.get(username='yaseen')
        q = Question(question_text=text, pub_date=dt, owner=yaseen)
        q.save()

        return HttpResponse("The question you entered was: " + str(text) + "? at " + str(dt))

    context = {'text':text}
    return render(request, 'qpanda/question.html', context)

def askedquestion(request, question_id):

    q = Question.objects.get(pk=question_id)
    return HttpResponse("The question is: " + q.question_text)