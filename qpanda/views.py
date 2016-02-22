from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import QuestionForm, AnswerForm, UserForm
from .models import Question, Answer
from utils import gen_valid_pk


def index(request):
    return render(request, 'qpanda/index.html')


def askquestion(request):
    return render(request, 'qpanda/askquestion.html', {'questionform': QuestionForm(),
                                                       'userform': UserForm()})


def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['question_text']
        else:
            context = {'error': 'Please enter a valid question.',
                       'questionform': QuestionForm(),
                       'userform': UserForm()}
            return render(request, 'qpanda/askquestion.html', context)

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
        context = {'error': 'Question not found.',
                   'questionform': QuestionForm(),
                   'userform': UserForm()}
        return render(request, 'qpanda/askquestion.html', context)

    context = {'question_text': q.question_text,
               'question_id': q.id,
               'question_date': q.pub_date,
               'user_asking': q.owner.get_username(),
               'answerform': AnswerForm(),
               'answers': q.answer_set.order_by('-pub_date')[:10],
               'userform': UserForm()}

    return render(request, 'qpanda/askedquestion.html', context)


def answerquestion(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        try:
            q = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            context = {'error': 'Question not found.',
                       'form': QuestionForm()}
            return render(request, 'qpanda/askquestion.html', context)

        if form.is_valid():
            text = form.cleaned_data['answer_text']
        else:
            context = {'question_text': q.question_text,
                       'question_id': q.id,
                       'question_date': q.pub_date,
                       # Maybe I should just pass a question object, that only makes too much sense.
                       'error': 'Please enter a valid answer.',
                       'user_asking': q.owner.get_username(),
                       'answerform': AnswerForm(),
                       'answers': q.answer_set.order_by('-pub_date')[:10],
                       'userform': UserForm()}

            return render(request, 'qpanda/askedquestion.html', context)

        a = Answer(question=q, answer_text=text, pub_date=timezone.now())
        a.save()

        return redirect('askedquestion', question_id=question_id)

    # when the user just enters the url qpanda.co/abcdefg/answer without submitting anything
    else:
        return redirect('askedquestion', question_id=question_id)


def login(request):
    print 'in login view'
    return HttpResponse("LOGIN")


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            print 'username: ' + form.cleaned_data['username']
            print 'password: ' + form.cleaned_data['password']
        else:
            """
            I'm so proud of myself right now. I think this moment has now solidified my career in computer science.

            I spent atleast an hour trying to figure out how to view the validation error that occurs when is_valid()
            fails. I only want the error message itself, not '[ValidationError([u'This field is required.'])]' or the
            error message encased in the default django html error tags. I would have loved to get the errormessage and
            then display it in my own error div or something, but instead I have to do some hacking (I've actually got a
            Han Solo like smirk on my face right now because I'm so proud of my shortcut).

            Anyways I did it. I'm going to make it as a software developer now. #hacktheplanet
            """

            firsterrorkey = form.errors.keys()[0]
            # could be multiple errors, we don't want to overwhelm the user so we'll just display one.
            errordict = form.errors.as_data()
            # this returns a dict instead of enclosing the error in a html tags.
            errormsg = unicode(errordict[firsterrorkey])[20:-4]
            print firsterrorkey + ' error: ' + errormsg
            # and boom we've got the error message.

            """
            It's been a few minutes since I came up with my very unsafe solution that made me super proud. But I have
            some kind of post-hack depression. Because I know that I can't use this in a real environment. It's super
            sad. But I will commit this and I hope somebody will eventually read this and realise my genius (stupidity).
            """

        # TODO Fix username/password validation e.g. no symbols in username.
        # TODO Add Try/Except block to see if username already exists in db.

        # using the userform will now check if it is valid, however I think I need to include a try/except block still.
        # the try/except block will accept a ValidationError.
        # should now be able to use form.is_valid() like the other views.

    return HttpResponse("REGISTER")
