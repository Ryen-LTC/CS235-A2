from typing import List, Iterable
from movies.adapters.repository import AbstractRepository
from movies.adapters.memory_repository import MemoryRepository
from movies.adapters.memory_repository import load_movies
from movies.domain.model import Actor, Movie, Genre, Director, Review, User, Comment, make_comment


class UnknownUserException(Exception):
    pass


class NonExistentMovieException(Exception):
    pass


def get_all_movies(repo: AbstractRepository):
    res = repo.get_all_movies()
    return res


def get_movies_by_actor(repo: AbstractRepository, name: str):
    res = repo.get_movie_by_actor(name)
    return res


def get_movies_by_genre(repo: AbstractRepository, genre: str):
    res = repo.get_movie_by_genre(genre)
    return res


def get_movies_by_director(repo: AbstractRepository, director: str):
    res = repo.get_movie_by_director(director)
    return res


def get_movie_by_rank(repo: AbstractRepository, rank: int):
    res = repo.get_movie_by_rank(rank)
    return res


def add_comment(movie_rank: int, comment_text: str, username: str, repo: AbstractRepository):
    # Check that the article exists.
    movie = repo.get_movie_by_rank(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, movie)

    # Update the repository.
    repo.add_comment(comment)


def get_comments_for_movie(movie_rank: int, repo: AbstractRepository):
    movie = repo.get_movie_by_rank(movie_rank)

    if movie is None:
        raise NonExistentMovieException

    return comments_to_dict(movie.comments)


def comment_to_dict(comment: Comment):
    comment_dict = {
        'username': comment.user.user_name,
        'movie_id': comment.movie.rank,
        'comment_text': comment.comment,
        'timestamp': comment.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Comment]):
    return [comment_to_dict(comment) for comment in comments]
