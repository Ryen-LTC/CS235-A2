from flask import Blueprint, request, render_template, redirect, url_for, session
from flask import current_app as app

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from better_profanity import profanity

import movies.adapters.repository as repo
import movies.movie.services as services
from movies.authentication.authentication import login_required
import random

movie_blueprint = Blueprint('movie_bp', __name__)


@movie_blueprint.route('/movies', methods=['GET'])
def show_all_movies():
    movies_per_page = 5

    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    form = SearchForm()
    form.cursor.data = 0

    keywords = request.args.get("keywords")
    searchType = request.args.get("searchType")

    if keywords is None or keywords.strip() == "":
        keywords = ''

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
        else:
            movies = services.get_all_movies(repo.repo_instance)
    else:
        movies = services.get_all_movies(repo.repo_instance)

    total_movies = len(movies)
    movies = movies[cursor:cursor + movies_per_page]

    first_page_url = None
    last_page_url = None
    next_page_url = None
    prev_page_url = None

    if cursor > 0:
        if not filtered:
            prev_page_url = url_for('movie_bp.show_all_movies', cursor=cursor - movies_per_page)
            first_page_url = url_for('movie_bp.show_all_movies')
        else:
            prev_page_url = url_for('movie_bp.show_all_movies', keywords=keywords, searchType=searchType,
                                    cursor=cursor - movies_per_page)
            first_page_url = url_for('movie_bp.show_all_movies', keywords=keywords, searchType=searchType)

    if cursor + movies_per_page < total_movies:
        if not filtered:
            next_page_url = url_for('movie_bp.show_all_movies', cursor=cursor + movies_per_page)
            last_cursor = movies_per_page * int(total_movies / movies_per_page)
            if total_movies % movies_per_page == 0:
                last_cursor -= movies_per_page
            last_page_url = url_for('movie_bp.show_all_movies', cursor=last_cursor)
        else:
            next_page_url = url_for('movie_bp.show_all_movies', keywords=keywords, searchType=searchType,
                                    cursor=cursor + movies_per_page)
            last_cursor = movies_per_page * int(total_movies / movies_per_page)
            if total_movies % movies_per_page == 0:
                last_cursor -= movies_per_page
            last_page_url = url_for('movie_bp.show_all_movies', keywords=keywords, searchType=searchType,
                                    cursor=last_cursor)

    return render_template('movie/movies.html',
                           movies_list=movies,
                           form=form,
                           handler_url=url_for('movie_bp.show_all_movies'),
                           cursor=cursor,
                           keywords=keywords,
                           searchType=searchType,
                           first_page_url=first_page_url,
                           last_page_url=last_page_url,
                           next_page_url=next_page_url,
                           prev_page_url=prev_page_url,
                           random_num_list=get_random_list(),
                           sidebar_movies=get_sidebar_movies()
                           )


@movie_blueprint.route('/movies/detail', methods=['GET'])
def show_movie_details():
    rank = request.args.get('rank')
    movie = services.get_movie_by_rank(repo.repo_instance, int(rank))

    cursor = request.args.get('cursor')
    keywords = request.args.get("keywords")
    searchType = request.args.get("searchType")

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    if keywords is None or keywords.strip() == "":
        prev_page_url = url_for('movie_bp.show_all_movies', cursor=cursor)
        add_comment_url = url_for('movie_bp.comment_on_movie', rank=rank, cursor=cursor)
    else:
        prev_page_url = url_for('movie_bp.show_all_movies',
                                keywords=keywords,
                                searchType=searchType,
                                cursor=cursor
                                )
        add_comment_url = url_for('movie_bp.comment_on_movie',
                                  rank=rank,
                                  keywords=keywords,
                                  searchType=searchType,
                                  cursor=cursor
                                  )

    return render_template('movie/details.html',
                           movie=movie,
                           add_comment_url=add_comment_url,
                           prev_page_url=prev_page_url,
                           random_num_list=get_random_list(),
                           sidebar_movies=get_sidebar_movies()
                           )


@movie_blueprint.route('/movies/detail/comment', methods=['GET', 'POST'])
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
        keywords = form.keywords.data
        searchType = form.searchType.data
        cursor = int(form.cursor.data)

        # Use the service layer to store the new comment.
        services.add_comment(movie_rank, form.comment.data, username, repo.repo_instance)

        # Retrieve the article in dict form.
        movie = services.get_movie_by_rank(repo.repo_instance, movie_rank)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        if keywords is None or keywords.strip() == '':
            return redirect(url_for('movie_bp.show_movie_details',
                                    rank=movie_rank,
                                    cursor=cursor))
        else:
            return redirect(url_for('movie_bp.show_movie_details',
                                    rank=movie_rank,
                                    keywords=keywords,
                                    searchType=searchType,
                                    cursor=cursor))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the article id, representing the article to comment, from a query parameter of the GET request.
        movie_rank = int(request.args.get('rank'))
        keywords = request.args.get('keywords')
        searchType = request.args.get('searchType')
        cursor = int(request.args.get('cursor'))

        # Store the article id in the form.
        form.movie_rank.data = movie_rank
        form.keywords.data = keywords
        form.searchType.data = searchType
        form.cursor.data = cursor
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_rank = int(form.movie_rank.data)
        keywords = form.keywords.data
        searchType = form.searchType.data
        cursor = int(form.cursor.data)

    # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    movie = services.get_movie_by_rank(repo.repo_instance, movie_rank)

    return render_template(
        'movie/comment_on_movie.html',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.comment_on_movie'),
        cursor=cursor,
        keywords=keywords,
        searchType=searchType,
        random_num_list=get_random_list(),
        sidebar_movies=get_sidebar_movies()
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

    movie_rank = HiddenField('Rank')
    keywords = HiddenField('Keywords')
    searchType = HiddenField('SearchType')
    cursor = HiddenField('Cursor')
    submit = SubmitField('Submit')


# Sidebar movies
def get_random_list():
    random_list = random.sample(range(1, 11), 4)
    return random_list


def get_sidebar_movies():
    sidebar_movies = dict()

    sidebar_movies[1] = ['Baby Done', "https://www.eventcinemas.co.nz/Movie/Baby-Done",
                         url_for('static', filename='movie1.jpg')]
    sidebar_movies[2] = ['Honest Thief', "https://www.eventcinemas.co.nz/Movie/Honest-Thief",
                         url_for('static', filename='movie2.jpg')]
    sidebar_movies[3] = ['The War with Grandpa', "https://www.eventcinemas.co.nz/Movie/The-War-With-Grandpa",
                         url_for('static', filename='movie3.jpg')]
    sidebar_movies[4] = ['The Secret Garden', "https://www.eventcinemas.co.nz/Movie/The-Secret-Garden",
                         url_for('static', filename='movie4.jpg')]
    sidebar_movies[5] = ['Savage', 'https://www.eventcinemas.co.nz/Movie/Savage',
                         url_for('static', filename='movie5.jpg')]
    sidebar_movies[6] = ['100% Wolf', 'https://www.eventcinemas.co.nz/Movie/100-Percent-Wolf',
                         url_for('static', filename='movie6.jpg')]
    sidebar_movies[7] = ['Cats & Dogs 3: Paws Unite', 'https://www.eventcinemas.co.nz/Movie/Cats--Dogs-3-Paws-Unite',
                         url_for('static', filename='movie7.jpg')]
    sidebar_movies[8] = ['Tenet', 'https://www.eventcinemas.co.nz/Movie/Tenet',
                         url_for('static', filename='movie8.jpg')]
    sidebar_movies[9] = ['Astro Kid', 'https://www.eventcinemas.co.nz/Movie/Astro-Kid',
                         url_for('static', filename='movie9.jpg')]
    sidebar_movies[10] = ['My People, My Homeland', 'https://www.eventcinemas.co.nz/Movie/My-People-My-Homeland',
                          url_for('static', filename='movie10.jpg')]

    return sidebar_movies
