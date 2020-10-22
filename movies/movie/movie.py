from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
from movies.domain.model import Actor, Movie, Genre, Director, Review, User
from movies.adapters.repository import AbstractRepository
from movies.adapters.memory_repository import MemoryRepository

import movies.adapters.repository as repo
import movies.movie.services as services

movie_blueprint = Blueprint('movie_bp', __name__)


@movie_blueprint.route('/all_movies', methods=['GET'])
def show_all_movies():
    movies_per_page = 15

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
        movies_list=movies,
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url,
    )


@movie_blueprint.route('/details', methods=['GET'])
def show_movie_details():
    name = request.args.get('title')
    year = request.args.get('year')
    movie = Movie(name, int(year))
    actors = services.get_actors(repo.repo_instance)
    return render_template('movie/details.html',
                           title=name,
                           year=year,
                           movie=movie,
                           actors=actors
                           )


