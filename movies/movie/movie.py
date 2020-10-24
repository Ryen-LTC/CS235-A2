from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from movies.domain.model import Actor, Movie, Genre, Director, Review, User, Comment, make_comment

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

import movies.adapters.repository as repo
import movies.movie.services as services

from flask import current_app as app

from movies.authentication.authentication import login_required

movie_blueprint = Blueprint('movie_bp', __name__)


@movie_blueprint.route('/all_movies', methods=['GET'])
def show_all_movies():
    movies_per_page = 5

    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    total_movies = len(services.get_all_movies(repo.repo_instance))
    movies = services.get_all_movies(repo.repo_instance)[cursor:cursor + movies_per_page]

    first_page_url = None
    last_page_url = None
    next_page_url = None
    prev_page_url = None

    if cursor > 0:
        prev_page_url = url_for('movie_bp.show_all_movies', cursor=cursor - movies_per_page)
        first_page_url = url_for('movie_bp.show_all_movies')

    if cursor + movies_per_page < total_movies:
        next_page_url = url_for('movie_bp.show_all_movies', cursor=cursor + movies_per_page)
        last_cursor = movies_per_page * int(total_movies / movies_per_page)
        if total_movies % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_page_url = url_for('movie_bp.show_all_movies', cursor=last_cursor)

    return render_template(
        'movie/movies.html',
        handler_url=url_for('movie_bp.show_all_movies'),
        cursor=cursor,
        movies_list=movies,
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
    )


@movie_blueprint.route('/search_movies', methods=['GET'])
def search_movies():
    form = SearchForm()
    keywords = request.args.get("keywords")
    searchType = request.args.get("searchType")

    app.logger.info('keywords: %s | searchType: %s', keywords, searchType)

    movies = []
    filtered = False

    if keywords is not None and keywords.strip() != "":
        if searchType == "Actor":
            filtered = True
            movies = services.get_movies_by_actor(repo.repo_instance, keywords)
        elif searchType == "Genre":
            filtered = True
            movies = services.get_movies_by_genre(repo.repo_instance, keywords)
        elif searchType == "Director":
            filtered = True
            movies = services.get_movies_by_director(repo.repo_instance, keywords)

    return render_template('movie/search_movies.html',
                           form=form,
                           handler_url=url_for('movie_bp.search_movies'),
                           movies_list=movies)


@movie_blueprint.route('/movie/details', methods=['GET'])
def show_movie_details():
    rank = request.args.get('rank')
    movie = services.get_movie_by_rank(repo.repo_instance, int(rank))

    cursor = request.args.get('cursor')
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    return render_template('movie/details.html',
                           movie=movie,
                           add_comment_url=url_for('movie_bp.comment_on_movie', rank=rank, cursor=cursor),
                           prev_page_url=url_for('movie_bp.show_all_movies', cursor=cursor)
                           )


@movie_blueprint.route('/movie/details/comment', methods=['GET', 'POST'])
@login_required
def comment_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
    # form.
    form = CommentForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        movie_rank = int(form.movie_rank.data)
        cursor = int(form.cursor.data)

        # Use the service layer to store the new comment.
        services.add_comment(movie_rank, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        movie = services.get_movie_by_rank(repo.repo_instance, movie_rank)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('movie_bp.show_movie_details', rank=movie_rank, cursor=cursor))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_rank = int(request.args.get('rank'))
        cursor = int(request.args.get('cursor'))

        # Store the article id in the form.
        form.movie_rank.data = movie_rank
        form.cursor.data = cursor
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_rank = int(form.movie_rank.data)
        cursor = int(form.cursor.data)
    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie_by_rank(repo.repo_instance, movie_rank)

    return render_template(
        'movie/comment_on_movie.html',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.comment_on_movie'),
    )


class SearchForm(FlaskForm):
    keywords = StringField('Keywords')
    searchType = SelectField('SearchType', choices=[
        'Actor',
        'Genre',
        'Director',
    ])
    cursor = HiddenField('Cursor')
    submit = SubmitField('Search')


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    movie_rank = HiddenField('Movie rank')
    cursor = HiddenField('Cursor')
    submit = SubmitField('Submit')
