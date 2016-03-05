from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime

# We use a get parameter to return to a specific url after a form submit, but we don't want to redirect to a url which
# we use for a POST submit.
dont_redirect_here = ['/login/', '/answer/', '/register/', '/qpanda/question/']

def gen_valid_pk():
    # We don't want a primary key for a Question to start with the letter t, as questions which start with t will be
    # reserved for temporary questions e.g. qpanda.co/tA83zqP will be a temporary question. But we're not going to
    # removed t from allowed_chars that get_random_string() can take as a parameter because 't' can appear later on.
    # e.g. qpanda.co/t123456 is invalid, qpanda.co/1234t56 is okay.

    pk = get_random_string(length=7)
    while pk[0] == 't':
        pk = get_random_string(length=7)
    return pk


def json_encode_answer(answers, more_answers=False):
    # question.answer_set() returns a python set and not a list (I believe?). The Django JSON Encoder cannot encode a
    # a set, so we choose what to fields to encode into a python dict. The django docs recommend using your own encoder
    # but I think this might be easier.
    answers_dict = {}

    for i in range(len(answers)):
        # the list answers passed into this function is a sorted list. Dicts are not sorted, so instead we will choose
        # with keys which we can sort client side. I haven't sorted them client side though yet because I think a for
        # loop over javascript objects keys will sort them automatically (REALLY REALLY NEED TO CHECK THIS OUT THOUGH).

        a = answers[i]
        answers_dict[i] = {'username': a.owner.get_username(),
                           'pub_date': a.pub_date,
                           'time_since': naturaltime(a.pub_date),
                           'answer_text': a.answer_text}

    # TODO Include time since asked?
    # Should we calculate the time since the question was asked server or client side

    json_dict = {'answers': answers_dict,
                 'more_answers': more_answers}

    return json_dict
