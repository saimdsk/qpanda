from django.utils.crypto import get_random_string
from django.utils import timezone

import pytz

def gen_valid_pk():
    # We don't want a primary key for a Question to start with the letter t, as questions which start with t will be
    # reserved for temporary questions e.g. qpanda.co/tA83zqP will be a temporary question. But we're not going to
    # removed t from allowed_chars that get_random_string() can take as a parameter because 't' can appear later on.
    # e.g. qpanda.co/t123456 is invalid, qpanda.co/1234t56 is okay.

    pk = get_random_string(length=7)
    while pk[0] == 't':
        pk = get_random_string(length=7)
    return pk


def get_usertz(request):
    tz = None
    try:
        tz = request.session['usertz']
    except KeyError:
        pass

    return tz


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get('usertz')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
