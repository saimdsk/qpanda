from django.utils.crypto import get_random_string

def gen_valid_pk():
    # We don't want a primary key for a Question to start with the letter t, as questions which start with t will be
    # reserved for temporary questions e.g. qpanda.co/tA83zqP will be a temporary question. But we're not going to
    # removed t from allowed_chars that get_random_string() can take as a parameter because 't' can appear later on.
    # e.g. qpanda.co/t123456 is invalid, qpanda.co/1234t56 is okay.

    # TODO Unique key collision
    # I'm not sure whether I should do it here or in a view, but there is going to be the eventuality that this function
    # will generate a pk that already exists in the database. I'm not sure if I should query the database everytime
    # to see if the pk already exists. That will be superfluous because it will be for every single time this function
    # is called. I could instead wait for a django.db.IntegrityError which will be raised when another question tries to
    # use the same id. Yeah that makes more sense. I'll do that. I'm going to submit another fix first before I do that.

    pk = get_random_string(length=7)
    while pk[0] == 't':
        pk = get_random_string(length=7)
    return pk
