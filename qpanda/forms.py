import re

from django import forms
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

    def clean_username(self):
        # when form.is_valid() is called, clean_username will also be called allowing for custom validation.

        data = self.cleaned_data['username']
        rules = re.compile(u'^[a-zA-Z-_][a-zA-Z0-9-_]{4,}$')
        # username must start with a letter or '-' or '_'.
        # It can only contain letters, numbers, '-', and '_'.
        # It must be atleast 5 characters long.
            # we use {4,} because it only checks that the closest [] is x characters long.
        if rules.match(data) is None:
            # failed the regex.
            if len(data) < 5:
                raise forms.ValidationError('Username is not long enough.')
            elif unicode.isnumeric(data[0]):
                raise forms.ValidationError('Username must start with a letter, hyphen, or underscore.')
            else:
                raise forms.ValidationError('Username can only contain letters, numbers, hyphens, or underscores.')

        return data

    def clean_password(self):
        data = self.cleaned_data['password']

        if len(data) < 6:
            raise forms.ValidationError('Password is not long enough.')

        return data


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

