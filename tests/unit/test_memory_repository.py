from datetime import date, datetime
from typing import List

import pytest

from movies.adapters.memory_repository import MemoryRepository
from movies.adapters.repository import AbstractRepository, RepositoryException
from movies.domain.model import Movie, Actor, Director, Genre, Review, User


# User
def test_add_user(in_memory_repo):
    assert in_memory_repo.get_user_size() == 2
    in_memory_repo.add_user(User('a', '123'))
    assert in_memory_repo.get_user_size() == 3
    in_memory_repo.add_user(User('a', '123'))
    assert in_memory_repo.get_user_size() == 3
    in_memory_repo.add_user(User('b', '456'))
    assert in_memory_repo.get_user_size() == 4


def test_get_user(in_memory_repo):
    user = User('Tom', '123')
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user('Tom') == user


# Actor
def test_add_actor(in_memory_repo):
    assert in_memory_repo.get_actor_size() == 0
    actor1 = Actor('a')
    in_memory_repo.add_actor(actor1)
    assert in_memory_repo.get_actor_size() == 1
    in_memory_repo.add_actor(actor1)
    assert in_memory_repo.get_actor_size() == 1
    actor2 = Actor('b')
    in_memory_repo.add_actor(actor2)
    assert in_memory_repo.get_actor_size() == 2


def test_get_actor(in_memory_repo):
    actor1 = Actor('a')
    actor2 = Actor('b')
    in_memory_repo.add_actor(actor1)
    in_memory_repo.add_actor(actor2)
    assert in_memory_repo.get_actor('a') == actor1
    assert in_memory_repo.get_actor('b') == actor2
    assert in_memory_repo.get_actor('b') != actor1


# Director
def test_add_director(in_memory_repo):
    assert in_memory_repo.get_director_size() == 0
    director1 = Director('a')
    director2 = Director('b')
    in_memory_repo.add_director(director1)
    assert in_memory_repo.get_director_size() == 1
    in_memory_repo.add_director(director1)
    assert in_memory_repo.get_director_size() == 1
    in_memory_repo.add_director(director2)
    assert in_memory_repo.get_director_size() == 2


def test_get_director(in_memory_repo):
    director1 = Director('a')
    director2 = Director('b')
    in_memory_repo.add_director(director1)
    in_memory_repo.add_director(director2)
    assert in_memory_repo.get_director('a') == director1
    assert in_memory_repo.get_director('b') == director2
    assert in_memory_repo.get_director('b') != director1


# Genre
def test_add_genre(in_memory_repo):
    assert in_memory_repo.get_genre_size() == 0
    genre1 = Genre('a')
    in_memory_repo.add_genre(genre1)
    assert in_memory_repo.get_genre_size() == 1
    genre2 = Genre('b')
    in_memory_repo.add_genre(genre2)
    assert in_memory_repo.get_genre_size() == 2
    in_memory_repo.add_genre(genre1)
    assert in_memory_repo.get_genre_size() == 2


def test_get_genre(in_memory_repo):
    genre1 = Genre('a')
    genre2 = Genre('b')
    in_memory_repo.add_genre(genre1)
    in_memory_repo.add_genre(genre2)
    assert in_memory_repo.get_genre('a') == genre1
    assert in_memory_repo.get_genre('b') == genre2
    assert in_memory_repo.get_genre('b') != genre1


# Movie
def test_add_movie(in_memory_repo):
    assert in_memory_repo.get_movie_size() == 10
    movie1 = Movie('a', 2000)
    in_memory_repo.add_movie(movie1)
    assert in_memory_repo.get_movie_size() == 11
    in_memory_repo.add_movie(movie1)
    assert in_memory_repo.get_movie_size() == 11
    movie2 = Movie('a', 1999)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_size() == 12


def test_get_movie_by_name(in_memory_repo):
    movie1 = Movie('Sing', 3000)
    in_memory_repo.add_movie(movie1)
    assert in_memory_repo.get_movie_by_name('Sing') == [Movie('Sing', 2016), movie1]
    movie2 = Movie('Sing', 2000)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_name('Sing') == [movie2, Movie('Sing', 2016), movie1]


def test_get_movie_by_year(in_memory_repo):
    assert len(in_memory_repo.get_movie_by_year(2016)) == 8
    movie = Movie('a', 2016)
    in_memory_repo.add_movie(movie)
    assert len(in_memory_repo.get_movie_by_year(2016)) == 9


def test_get_movie_by_name_and_year(in_memory_repo):
    assert in_memory_repo.get_movie_by_name_and_year('Sing', 2016) == [Movie('Sing', 2016)]
    movie1 = Movie('a', 2000)
    movie2 = Movie('a', 3000)
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_name_and_year('a', 2000) != [movie2]


def test_get_movie_by_actor(in_memory_repo):
    assert in_memory_repo.get_movie_by_actor('Chris Pratt') == [Movie('Guardians of the Galaxy', 2014),
                                                                Movie('Passengers', 2016)]
    movie1 = Movie('1', 2000)
    movie2 = Movie('2', 3000)
    actor1 = Actor('a')
    movie1.add_actor(actor1)
    movie2.add_actor(actor1)
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_actor('a') == [movie1, movie2]


def test_get_movie_by_genre(in_memory_repo):
    assert in_memory_repo.get_movie_by_genre('Action') == [Movie('Guardians of the Galaxy', 2014),
                                                           Movie('Suicide Squad', 2016),
                                                           Movie('The Great Wall', 2016),
                                                           Movie('The Lost City of Z', 2016)]
    movie1 = Movie('1', 2000)
    movie2 = Movie('2', 3000)
    genre1 = Genre('a')
    movie1.add_genre(genre1)
    movie2.add_genre(genre1)
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_genre('a') == [movie1, movie2]


def test_get_movie_by_director(in_memory_repo):
    assert in_memory_repo.get_movie_by_director('M. Night Shyamalan') == [Movie('Split', 2016)]
    movie1 = Movie('1', 2000)
    movie2 = Movie('2', 3000)
    director1 = Director('a')
    movie1.director = director1
    movie2.director = director1
    in_memory_repo.add_movie(movie1)
    in_memory_repo.add_movie(movie2)
    assert in_memory_repo.get_movie_by_director('a') == [movie1, movie2]