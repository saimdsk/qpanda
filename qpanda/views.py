from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import QuestionForm, AnswerForm, UserForm
from .models import Question, Answer
from utils import gen_valid_pk, json_encode_answer


def index(request):
    return render(request, 'qpanda/index.html')


def handler404(request, error='Something went wrong...'):
    context = {'mainerror': error,
               'questionform': QuestionForm(),
               'userform': UserForm()}
    return render(request, 'qpanda/askquestion.html', context)


def askquestion(request):
    return render(request, 'qpanda/askquestion.html', {'questionform': QuestionForm(),
                                                       'userform': UserForm()})


def nextURL(request):
    nexturl = request.GET.get('next')

    if nexturl is not None:
        return redirect(nexturl)
    else:
        return redirect('askquestion')


def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['question_text']
        else:
            return handler404(request, error='Please enter a valid question.')

        if request.user.is_authenticated():
            owner = request.user
        else:
            owner = None

        question = Question.create(question_text=text, owner=owner)

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
        return redirect('askquestion')


def askedquestion(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return handler404(request, error='Question not found.')

    context = {'question': question,
               'answerform': AnswerForm(),
               'answers': question.answer_set.order_by('-pub_date')[:10],
               'userform': UserForm()}

    return render(request, 'qpanda/askedquestion.html', context)


def answerquestion(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return handler404(request, error='Question not found.')

        if form.is_valid():
            text = form.cleaned_data['answer_text']
        else:
            context = {'question': question,
                       'mainerror': 'Please enter a valid answer.',
                       'user_asking': question.owner.get_username(),
                       'answerform': AnswerForm(),
                       'answers': question.answer_set.order_by('-pub_date')[:10],
                       'userform': UserForm()}

            # TODO Redirect to askedquestion and figure out how pass error data.
            # this still loads qpanda.co/abc1234/answer. Reloading this page will resubmit the invalid form data.
            # Instead we should just hand redirect this to askedquestion. I don't like it when a website tells me that
            # when I'm reloading a page, I'm resubmitting data. Fix this. I did spend time earlier trying to figure out
            # how to redirect and pass an error but gave up, because it became too difficult. I think I need to
            # reattempt finding a solution.
            return render(request, 'qpanda/askedquestion.html', context)

        if request.user.is_authenticated():
            owner = request.user
        else:
            owner = None

        a = Answer(question=question, answer_text=text, pub_date=timezone.now(), owner=owner)
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
            return nextURL(request)
        else:
            return HttpResponse("Incorrect username/password.")

    else:
        # Display a page that a user can use to login. This can be the same as the one in the register view.
        print 'have to include something in this else if block.'
        return HttpResponse("Have to do something.")


def user_logout(request):
    logout(request)
    return nextURL(request)


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username)
            user.set_password(raw_password=password)
            # we use set_password because that calls the hash function, using password= in the User constructor doesn't.
            user.save()

            loggedinuser = authenticate(username=username, password=password)
            login(request, loggedinuser)
            return nextURL(request)

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


def ajax_more_answers(request, question_id):
    if request.is_ajax():
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return HttpResponse(status=404)

        from_answer = int(request.GET.get('from'))
        if from_answer is None:
            from_answer = 0

        answers = question.answer_set.order_by('-pub_date')[from_answer:]

        encoded = json_encode_answer(answers)
        response = JsonResponse(encoded)

        return response

    else:
        return handler404(request)


