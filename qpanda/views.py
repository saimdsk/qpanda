from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer
from utils import gen_valid_pk


def index(request):
    return render(request, 'qpanda/index.html')


def askquestion(request):
    form = QuestionForm()
    return render(request, 'qpanda/askquestion.html', {'form':form})


def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['question_text']
        else:
            return render(request, 'qpanda/askquestion.html', {'error': 'Please enter a valid question.',
                                                               'form': QuestionForm()})

        # hard coded for now, will fix later.
        yaseen = User.objects.get(username='yaseen')

        question = Question.create(question_text=text, owner=yaseen)
        try:
            question.save()
        except IntegrityError:
            pk = gen_valid_pk()
            while pk in Question.objects.filter(id=pk):
                pk = gen_valid_pk()
            question.save()
        # there is a possibility (very slim) that gen_valid_pk() will generate the same unique key. If that happens when
        # you try to call save an IntegrityError will be raised. We just keep calling gen_valid_pk() until a unique key
        # is found. I don't want to check for this every time I generate a pk or in the model itself, so I'll include it
        # here, but I don't think that the except block will ever be called.

        return redirect('askedquestion', question_id=question.id)
        # once the question has been successfully saved we redirect to the askedquestion view to display it.

    else:
        return render(request, 'qpanda/index.html')


def askedquestion(request, question_id):
    try:
        q = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return render(request, 'qpanda/askquestion.html', {'error': 'Question not found.', 'form': QuestionForm()})

    context = {'question': q.question_text,
               'form': AnswerForm(),
               'question_id': q.id,
               'answers': q.answer_set.order_by('-pub_date')}
    return render(request, 'qpanda/askedquestion.html', context)


def answerquestion(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        try:
            q = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return render(request, 'qpanda/askquestion.html', {'error': 'Question not found.', 'form': QuestionForm()})

        if form.is_valid():
            text = form.cleaned_data['answer_text']
        else:
            context = {'question': q.question_text,
                       'form': AnswerForm(),
                       'question_id': q.id,
                       'answers': q.answer_set.all(),
                       'error': 'Please enter a valid answer.'}
            return render(request, 'qpanda/askedquestion.html', context)

        a = Answer(question=q, answer_text=text, pub_date=timezone.now())
        a.save()

        return redirect('askedquestion', question_id=question_id)

    # when the user just enters the url qpanda.co/abcdefg/answer without submitting anything
    else:
        try:
            q = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return render(request, 'qpanda/askquestion.html', {'error': 'Question not found.', 'form': QuestionForm()})

        return redirect('askedquestion', question_id=question_id)