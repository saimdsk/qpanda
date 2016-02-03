from django.db import models
from django.contrib.auth.models import User

from qpanda.utils import gen_valid_pk

class Question(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default=gen_valid_pk(), unique=True)
    # Instead of using numbers to identify questions, I will use random letters and numbers. Eventually qpanda.co will
    # be set up that will be a url shortener for the questions. We use what follows the slash as the question identifier
    # which keeps the urls short (instead of just using base10 integers which will fill up much faster) and makes it
    # more difficult to stumble across another users question. e.g. if you were assigned qpanda.co/213 you can just go
    # to qpanda.co/212 to look at another question. Django's get_random_string() will produce a random string made up of
    # 62 possible letters. 62**7 = 3 521 614 606 208L. So 3 trillion possible questions. Do you think that's enough?


    question_text = models.CharField(verbose_name='Question',max_length=200)
    # verbose name was added for when the QuestionForm is rendered

    pub_date = models.DateTimeField('date published')
    owner = models.ForeignKey(User, null=True)

    def __unicode__(self):
        if self.owner is None:
            return "Question: " + self.question_text
        else:
            return self.owner.get_username() + "'s Question: " + self.question_text


class PollChoice(models.Model):
    question = models.ForeignKey(Question)
    pollchoice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)