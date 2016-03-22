from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import QuestionForm, AnswerForm, UserForm
from .models import Question, Answer
from utils import gen_valid_pk, json_encode_answer, dont_redirect_here


def index(request):
    return render(request, 'qpanda/index.html')


# Used to display error messages.
def handler404(request, error=u'Something went wrong...'):
    context = {'mainerror': error,
               'questionform': QuestionForm(),
               'userform': UserForm()}
    return render(request, 'qpanda/askquestion.html', context)


# Display the main page allowing users to ask a question.
def ask_question(request):
    return render(request, 'qpanda/askquestion.html', {'questionform': QuestionForm(),
                                                       'userform': UserForm()})


# We use this to redirect. If a user logs in from the ask_question page we should return to the ask_question page. If we
# log in from the asked_question page we should return to that same question.
def next_URL(request):
    next_url = request.GET.get('next')

    if next_url is None or next_url in dont_redirect_here:
        return redirect('ask_question')
    else:
        return redirect(next_url)


# A question form will submit to this view. They will then be redirected to the asked_question page.
def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['question_text']
        else:
            return handler404(request, error=u'Please enter a valid question.')

        if request.user.is_authenticated():
            owner = request.user
        else:
            # we allow a user to ask a question anonymously.
            owner = None

        # Why we use the create class method is explained in the model.
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

        return redirect('asked_question', question_id=question.id)
        # once the question has been successfully saved we redirect to the asked_question view to display it.

    else:
        return redirect('ask_question')


# Display a question that has been asked and any accompanying answers.
def asked_question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return handler404(request, error=u'Question not found.')

    # We check for a get parameter to see if they have already scrolled past a certain number of answers.
    try:
        from_answer = int(request.GET.get('from'))
        if from_answer < 0 or from_answer is None:
            from_answer = 0
    except TypeError:
        from_answer = 0

    context = {'question': question,
               'answerform': AnswerForm(),
               'answers': question.answer_set.order_by('-pub_date')[from_answer:from_answer+10],
               'from_answer': from_answer+10,
               'userform': UserForm()}

    if from_answer + 10 < len(question.answer_set.order_by('-pub_date')):
        # If there are more than 10 answers we display a button allowing the user to send an AJAX for more answers.
        context['more_answers'] = True

    return render(request, 'qpanda/askedquestion.html', context)


# An answer will submit to this form. This will then redirect back to the asked_question view.
def answer_question(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)

        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return handler404(request, error=u'Question not found.')

        if form.is_valid():
            text = form.cleaned_data['answer_text']
        else:
            context = {'question': question,
                       'mainerror': 'Please enter a valid answer.',
                       'user_asking': question.owner.get_username(),
                       'answerform': AnswerForm(),
                       'answers': question.answer_set.order_by('-pub_date')[:10],
                       'userform': UserForm()}

            # TODO Do redirect instead of making dict with error message.
            # this still loads qpanda.co/abc1234/answer. Reloading this page will resubmit the invalid form data.
            # Instead we should just hand redirect this to asked_question. I don't like it when a website tells me that
            # when I'm reloading a page, I'm resubmitting data. Fix this. I did spend time earlier trying to figure out
            # how to redirect and pass an error but gave up, because it became too difficult. I think I need to
            # reattempt finding a solution.
            return render(request, 'qpanda/askedquestion.html', context)

        if request.user.is_authenticated():
            owner = request.user
        else:
            # The user is answering anonymously.
            owner = None

        a = Answer(question=question, answer_text=text, pub_date=timezone.now(), owner=owner)
        a.save()

        return redirect('asked_question', question_id=question_id)

    # For when the user types in the url without a form submit. This shouldn't happen but just in case.
    else:
        return redirect('asked_question', question_id=question_id)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # do I need to add a try/except block here for a KeyError?
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return next_URL(request)
        else:
            # TODO: Change handler404 to redirect to both asked_question and ask_question.
            # If the user was on an asked_question page before attempting to log in they should be redirected to that
            # same page. As of now we redirect to a standard 404 page.
            return HttpResponse("Incorrect username/password.")

    else:
        # In the case that the user manually enters qpanda.co/login we should still display a login page.
        context = {'questionform': QuestionForm(),
                   'userform': UserForm(),
                   'hardlogin': True}
        return render(request, 'qpanda/askquestion.html', context)


# The view called when a user logs out. (Yes I know pretty self explanatory).
def user_logout(request):
    logout(request)
    return next_URL(request)


# The view called on register form submit.
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

            logged_in_user = authenticate(username=username, password=password)
            login(request, logged_in_user)
            return next_URL(request)

        else:
            firsterrorkey = form.errors.keys()[0]
            # could be multiple errors, we don't want to overwhelm the user so we'll just display one.
            errordict = form.errors.as_data()
            # this returns a dict instead of enclosing the error in a html tags.
            errormsg = unicode(errordict[firsterrorkey])[20:-4]
            # and boom we've got the error message.

            # This is a hack. I did atleast 2 google searches and gave up figuring out how to de-encapsulate the
            # ValidationError.

            return handler404(request, errormsg)

    else:
        # If the user manually enters qpanda.co/register we should still display a register page.
        context = {'questionform': QuestionForm(),
                   'userform': UserForm(),
                   'hardregistration': True}
        return render(request, 'qpanda/askquestion.html', context)


# Used for an ajax request. Perhaps I should move these into their own django module/app. Maybe even set up a different
# server that handles AJAX instead of django.
def ajax_more_answers(request, question_id):
    if request.is_ajax():
        # django has a get_object_or_404 method that I should probably use...
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return HttpResponse(status=404)

        try:
            # In case the get parameter is left off in the javascript (it shouldn't be, but still).
            from_answer = int(request.GET.get('from'))
            if from_answer is None:
                from_answer = 0
        except TypeError:
            from_answer = 0

        answers = question.answer_set.order_by('-pub_date')[from_answer:from_answer+10]

        if len(answers) == 0:
            # There aren't any more answers.
            return HttpResponseBadRequest()

        if from_answer + 10 < len(question.answer_set.order_by('-pub_date')):
            more_answers = True
            # We use this as a flag. Javascript will remove the more answers button if there aren't any more answers.
        else:
            more_answers = False

        encoded = json_encode_answer(answers, more_answers)
        response = JsonResponse(encoded)

        return response

    else:
        return handler404(request)
