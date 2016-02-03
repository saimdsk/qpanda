from django.utils.crypto import get_random_string

def gen_valid_pk():
    # We don't want a primary key for a Question to start with the letter t, as questions which start with t will be
    # reserved for temporary questions e.g. qpanda.co/tA83zqP will be a temporary question.

    pk = get_random_string(length=7)
    while pk[0] == 't':
        pk = get_random_string(length=7)
    return pk