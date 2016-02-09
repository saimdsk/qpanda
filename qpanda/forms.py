from django.forms import ModelForm, TextInput

from .models import Question, PollChoice

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        # We only need to display the question text part of the form. The rest of the fields we assign server side.
        widgets = {
            'question_text': TextInput(attrs={'class':'askbar', 'placeholder':'Ask A Question'}),
            # Because of the way forms work I just pass the form into the template and it knows what to render. Amazing!
            # But if you wish to make changes to the html element attributes you have to do it here.
        }


class PollChoiceForm(ModelForm):
    class Meta:
        model = PollChoice
        fields = ['question', 'pollchoice_text', 'votes']


