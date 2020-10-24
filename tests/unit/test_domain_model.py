from datetime import date

from movies.domain.model import User, Movie, make_comment, ModelException

import pytest


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def movie():
    return Movie(1, 'Guardians of the Galaxy', 2014,
                 'A group of intergalactic criminals are forced to work together to \
                 stop a fanatical warrior from taking control of the universe.')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_make_comment_establishes_relationships(movie, user):
    comment_text = 'COVID-19 in the USA!'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Article knows about the Comment.
    assert comment in movie.comments

    # Check that the Comment knows about the Article.
    assert comment.movie is movie

