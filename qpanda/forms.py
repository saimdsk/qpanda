from django.forms import ModelForm

from .models import Question, PollChoice

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        # We only need to display the question text part of the form. The rest of the fields we assign server side.

class PollChoiceForm(ModelForm):
    class Meta:
        model = PollChoice
        fields = ['question', 'pollchoice_text', 'votes']


