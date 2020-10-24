from datetime import date

import pytest

from movies.authentication.services import AuthenticationException
from movies.authentication import services as auth_services
from movies.movie import services as movie_services
from movies.movie.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_comment(in_memory_repo):
    movie_rank = 3
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the comment.
    movie_services.add_comment(movie_rank, comment_text, username, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    comments_as_dict = movie_services.get_comments_for_movie(movie_rank, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
        None) is not None


def test_cannot_add_comment_for_non_existent_article(in_memory_repo):
    movie_rank = 11
    comment_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.add_comment(movie_rank, comment_text, username, in_memory_repo)


def test_cannot_add_comment_by_unknown_user(in_memory_repo):
    movie_rank = 3
    comment_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_comment(movie_rank, comment_text, username, in_memory_repo)


def test_get_comments_for_article(in_memory_repo):
    comments_as_dict = movie_services.get_comments_for_movie(1, in_memory_repo)

    # Check that 2 comments were returned for article with id 1.
    assert len(comments_as_dict) == 2

    # Check that the comments relate to the article whose id is 1.
    movie_rank = [comment['movie_id'] for comment in comments_as_dict]
    movie_rank = set(movie_rank)
    assert 1 in movie_rank and len(movie_rank) == 1


def test_get_comments_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        comments_as_dict = movie_services.get_comments_for_movie(11, in_memory_repo)


def test_get_comments_for_movie_without_comments(in_memory_repo):
    comments_as_dict = movie_services.get_comments_for_movie(2, in_memory_repo)
    assert len(comments_as_dict) == 0
