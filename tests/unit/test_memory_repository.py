from datetime import datetime

import pytest

from movies.adapters.repository import RepositoryException
from movies.domain.model import Movie, Actor, Director, Genre, User, Comment, make_comment


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_movie_size()
    # Check that the query returned 6 Articles.
    assert number_of_movies == 10


def test_add_movie(in_memory_repo):
    assert in_memory_repo.get_movie_size() == 10
    movie1 = Movie(99, "a", 2000, "description")
    in_memory_repo.add_movie(movie1)
    assert in_memory_repo.get_movie_size() == 11
    in_memory_repo.add_movie(movie1)
    assert in_memory_repo.get_movie_size() == 11
    movie2 = Movie(99, "a", 1999, "description")
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_size() == 12


def test_get_movie_by_year(in_memory_repo):
    assert len(in_memory_repo.get_movie_by_year(2016)) == 8


def test_get_movie_by_actor(in_memory_repo):
    assert in_memory_repo.get_movie_by_actor('Chris Pratt') == [Movie(1, 'Guardians of the Galaxy', 2014, "A group of \
                                                        intergalactic criminals are forced to work together\
                                                        to stop a fanatical warrior from taking control of\
                                                        the universe."),
                                                                Movie(10, 'Passengers', 2016, "A spacecraft \
                                                                traveling to a distant colony planet and \
                                                                transporting thousands of people has a \
                                                                malfunction in its sleep chambers. As a result, \
                                                                two passengers are awakened 90 years early.")]
    movie1 = Movie(11, '1', 2000, "a")
    movie2 = Movie(12, '2', 3000, "a")
    actor1 = Actor('a')
    movie1.add_actor(actor1)
    movie2.add_actor(actor1)
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_actor('a') == [movie1, movie2]


def test_get_movie_by_genre(in_memory_repo):
    assert in_memory_repo.get_movie_by_genre('Action') == [Movie(1, 'Guardians of the Galaxy', 2014, "A group of \
                                                        intergalactic criminals are forced to work together\
                                                        to stop a fanatical warrior from taking control of\
                                                        the universe."),
                                                           Movie(5, 'Suicide Squad', 2016, "A secret government agency\
                                                            recruits some of the most dangerous incarcerated \
                                                            super-villains to form a defensive task force. \
                                                            Their first mission: save the world from the apocalypse."),
                                                           Movie(6, 'The Great Wall', 2016, "European mercenaries \
                                                           searching for black powder become embroiled in the defense\
                                                            of the Great Wall of China against a horde of monstrous\
                                                             creatures."),
                                                           Movie(9, 'The Lost City of Z', 2016, "A true-life drama, \
                                                           centering on British explorer Col. Percival Fawcett, who\
                                                            disappeared while searching for a mysterious city in the\
                                                             Amazon in the 1920s.")]
    movie1 = Movie(11, '1', 2000, "a")
    movie2 = Movie(12, '2', 3000, "a")
    genre1 = Genre('a')
    movie1.add_genre(genre1)
    movie2.add_genre(genre1)
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_genre('a') == [movie1, movie2]


def test_get_movie_by_director(in_memory_repo):
    assert in_memory_repo.get_movie_by_director('M. Night Shyamalan') == [Movie(3, 'Split', 2016, "Three girls are\
                                                                        kidnapped by a man with a diagnosed 23 \
                                                                        distinct personalities. They must try to \
                                                                        escape before the apparent emergence of \
                                                                        a frightful new 24th.")]
    movie1 = Movie(11, '1', 2000, "b")
    movie2 = Movie(12, '2', 3000, "a")
    director1 = Director('a')
    movie1.director = director1
    movie2.director = director1
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_director('a') == [movie1, movie2]


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie1 = in_memory_repo.get_movie_by_rank(101)
    assert movie1 is None


def test_repository_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie_by_rank(1)
    comment = make_comment("Trump's onto it!", user, movie)
    in_memory_repo.add_comment(comment)
    assert comment in in_memory_repo.get_comments()


def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie_by_rank(2)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())
    with pytest.raises(RepositoryException):
        in_memory_repo.add_comment(comment)


def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie_by_rank(2)
    comment = Comment(None, movie, "Trump's onto it!", datetime.today())
    user.add_comment(comment)
    with pytest.raises(RepositoryException):
        # Exception expected because the Article doesn't refer to the Comment.
        in_memory_repo.add_comment(comment)


def test_repository_can_retrieve_comments(in_memory_repo):
    assert len(in_memory_repo.get_comments()) == 2
