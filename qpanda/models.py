from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from qpanda.utils import gen_valid_pk


class Question(models.Model):
    id = models.CharField(primary_key=True, max_length=20, unique=True)
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

    @classmethod
    def create(cls, question_text, owner):
        # Django doesn't want you to screw around with an __init__ class method. So instead you can use a model manager
        # or django provides this create method. Initially I had "default=gen_valid_pk()" for the models id field. But
        # that just called gen_valid_pk() once and set a default of 'ebYrUAp' for all questions. Now we'll call
        # Question.create() from a view (or wherever else) and it will take care of setting both the date and pk.

        q = cls(question_text=question_text, owner=owner, pub_date=timezone.now(), id=gen_valid_pk())
        return q

    def __unicode__(self):
        if self.owner is None:
            return "Question: " + self.question_text
        else:
            return self.owner.get_username() + "'s Question: " + self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question)
    answer_text = models.TextField(verbose_name='Answer')
