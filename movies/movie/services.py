from typing import List, Iterable
from movies.adapters.repository import AbstractRepository
from movies.adapters.memory_repository import MemoryRepository
from movies.adapters.memory_repository import load_movies
from movies.domain.model import Actor, Movie, Genre, Director, Review, User


class UnknownUserException(Exception):
    pass


class NonExistentMovieException(Exception):
    pass


def get_all_movies(repo: AbstractRepository):
    res = repo.get_all_movies()
    return res


def get_movie(name: str, year: int, repo: AbstractRepository):
    movie = repo.get_movie_by_name_and_year(name, year)
    return movie


def get_actors(repo: AbstractRepository):
    actors = repo.get_all_actors()
    return actors
