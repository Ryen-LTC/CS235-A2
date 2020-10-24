import abc
from typing import List
from datetime import date

from movies.domain.model import Movie, Actor, Director, Genre, Review, User, Comment

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    # User
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_size(self) -> int:
        raise NotImplementedError

    # Actor
    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_name: str) -> Actor:
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor_size(self) -> int:
        raise NotImplementedError

    # Director
    @abc.abstractmethod
    def add_director(self, director: Director):
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_name: str) -> Director:
        raise NotImplementedError

    @abc.abstractmethod
    def get_director_size(self) -> int:
        raise NotImplementedError

    # Genre
    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name: str) -> Genre:
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre_size(self) -> int:
        raise NotImplementedError

    # Movie
    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_rank(self, rank: int) -> Movie:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_name(self, movie_name: str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_year(self, release_year: int) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_name_and_year(self, movie_name: str, release_year: int) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_actor(self, actor_name: str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_genre(self, genre_name: str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_director(self, director_name: str) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_size(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_movies(self) -> list:
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, comment: Comment):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.comments:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.movie is None or comment not in comment.movie.comments:
            raise RepositoryException('Comment not correctly attached to an Article')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError
