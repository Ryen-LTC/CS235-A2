from movies.domain.model import Actor, User, Movie, Director, Genre,\
    Comment, make_comment

from datetime import date, datetime

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


def test_movie_construction(movie):
    assert movie.rank == 1
    assert movie.title == 'Guardians of the Galaxy'
    assert movie.release_year == 2014
    assert movie.description == 'A group of intergalactic criminals are forced to work together to \
                 stop a fanatical warrior from taking control of the universe.'
    assert movie.number_of_comments == 0
    assert repr(movie) == '<Movie Guardians of the Galaxy, 2014>'


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


def test_comment(user, movie):
    comment1 = Comment(user, movie, "comment text", datetime.fromisoformat('2020-03-15'))
    assert comment1.user == user
    assert comment1.movie == movie
    assert comment1.comment == "comment text"
    assert comment1.timestamp == datetime.fromisoformat('2020-03-15')
    assert comment1.user.user_name == 'dbowie'
    assert comment1.movie.rank == 1


def test_actor():
    actor1 = Actor("a")
    assert actor1.actor_full_name == "a"
    actor2 = Actor("b")
    actor3 = Actor("a")
    assert actor1 != actor2
    assert hash(actor1) != hash(actor2)
    assert actor2 > actor1
    assert actor1 < actor2
    assert actor1 == actor3
    assert repr(actor1) == '<Actor a>'


def test_director():
    director1 = Director("a")
    assert director1.director_full_name == "a"
    assert repr(director1) == "<Director a>"
    director2 = Director("b")
    director3 = Director("a")
    assert director1 != director2
    assert director1 == director3
    assert director1 < director2
    assert director2 > director1
    assert hash(director1) != hash(director2)


def test_genre():
    genre1 = Genre("a")
    assert genre1.genre_name == "a"
    assert repr(genre1) == "<Genre a>"
    genre2 = Genre("b")
    genre3 = Genre("a")
    assert genre2 > genre1
    assert genre1 < genre2
    assert genre1 == genre3
    assert genre1 != genre2
    assert hash(genre1) != hash(genre2)



