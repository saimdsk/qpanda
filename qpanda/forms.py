from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.models import User

from .models import Question, Answer


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': 'authenticate',
                                         'id': 'username',
                                         'placeholder': 'Username',
                                         'type': 'input'}),
            'password': TextInput(attrs={'class': 'authenticate',
                                         'id': 'password',
                                         'placeholder': 'Password',
                                         'type': 'password'})
            # password should perhaps use PasswordInput instead of TextInput. Need to look research differences.
        }


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        # We only need to display the question text part of the form. The rest of the fields we assign server side.
        widgets = {
            'question_text': TextInput(attrs={'class': 'askbar',
                                              'placeholder': 'Ask A Question',
                                              'autofocus': 'autofocus'}),
            # autofocus is a boolean attr in html. But we have to submit it as a dict entry in django.

            # Because of the way forms work I just pass the form into the template and it knows what to render. Amazing!
            # But if you wish to make changes to the html element attributes you have to do it here.
        }


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']
        widgets = {
            'answer_text': Textarea(attrs={'class': 'answerbar',
                                           'placeholder': 'Enter your answer',
                                           'autofocus': 'autofocus'})
        }

