
from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User

from .forms import QuestionForm
from .models import Question
from utils import gen_valid_pk

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

        # hard coded for now, will fix later.
        yaseen = User.objects.get(username='yaseen')

        q = Question.create(question_text=text, owner=yaseen)
        try:
            q.save()
        except IntegrityError:
            pk = gen_valid_pk()
            while pk in Question.objects.filter(id=pk):
                pk = gen_valid_pk()
            q.save()
        # there is a possibility (very slim) that gen_valid_pk() will generate the same unique key. If that happens when
        # you try to call save an IntegrityError will be raised. We just keep calling gen_valid_pk() until a unique key
        # is found. I don't want to check for this every time I generate a pk or in the model itself, so I'll include it
        # here, but I don't think that the except block will ever be called.

        return HttpResponse("The question you entered was: " + q.question_text + "? at " + str(q.pub_date))

    else:
        return render(request, 'qpanda/index.html')


def askedquestion(request, question_id):
    try:
        q = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return HttpResponse("Question id: '" + question_id + "' not found.")
    return render(request, 'qpanda/askedquestion.html', {'question':q.question_text})