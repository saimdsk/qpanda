from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
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
            context = {'mainerror': 'Please enter a valid question.',
                       'questionform': QuestionForm(),
                       'userform': UserForm()}
            # Refer to the to-do (yes I changed it so my IDE doesn't show this as a to-do) about using a redirect
            # instead of rendering a page that will resubmit invalid form data if the user reloads the page.
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
        context = {'mainerror': 'Question not found.',
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
            context = {'mainerror': 'Question not found.',
                       'form': QuestionForm()}
            return render(request, 'qpanda/askquestion.html', context)

        if form.is_valid():
            text = form.cleaned_data['answer_text']
        else:
            context = {'question_text': q.question_text,
                       'question_id': q.id,
                       'question_date': q.pub_date,
                       # Maybe I should just pass a question object, that only makes too much sense.
                       'mainerror': 'Please enter a valid answer.',
                       'user_asking': q.owner.get_username(),
                       'answerform': AnswerForm(),
                       'answers': q.answer_set.order_by('-pub_date')[:10],
                       'userform': UserForm()}

            # TODO Redirect to askedquestion and figure out how pass error data.
            # this still loads qpanda.co/abc1234/answer. Reloading this page will resubmit the invalid form data.
            # Instead we should just hand redirect this to askedquestion. I don't like it when a website tells me that
            # when I'm reloading a page, I'm resubmitting data. Fix this. I did spend time earlier trying to figure out
            # how to redirect and pass an error but gave up, because it became too difficult. I think I need to
            # reattempt finding a solution.
            return render(request, 'qpanda/askedquestion.html', context)

        a = Answer(question=q, answer_text=text, pub_date=timezone.now())
        a.save()

        return redirect('askedquestion', question_id=question_id)

    # when the user just enters the url qpanda.co/abcdefg/answer without submitting anything
    else:
        return redirect('askedquestion', question_id=question_id)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # do I need to add a try/except block here for a KeyError?
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("You are now logged in as: " + user.username)
        else:
            return HttpResponse("Incorrect username/password.")

    else:
        # Display a page that a user can use to login. This can be the same as the one in the register view.
        print 'have to include something in this else if block.'
        return HttpResponse("Have to do something.")


def user_logout(request):
    logout(request)
    return redirect('askquestion')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'])
            # form.is_valid() checks to make sure that the username is unique, so we don't need to check.
            user.set_password(form.cleaned_data['password'])
            # we use set_password because that calls the hash function, using password= in the User constructor doesn't.
            user.save()

            return HttpResponse('User: ' + user.username + ' with password: ' + user.password + ' created.')

        else:
            firsterrorkey = form.errors.keys()[0]
            # could be multiple errors, we don't want to overwhelm the user so we'll just display one.
            errordict = form.errors.as_data()
            # this returns a dict instead of enclosing the error in a html tags.
            errormsg = unicode(errordict[firsterrorkey])[20:-4]
            # and boom we've got the error message.
            print errormsg

    else:
        # need to write a regular register page where a user can sign up at. Not the main page.
        print 'have to include something in this if/else block.'

    return HttpResponse("REGISTER")
