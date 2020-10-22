import csv
import os

from movies.adapters.repository import AbstractRepository
from movies.domain.model import Movie, Actor, Director, Genre, User

from werkzeug.security import generate_password_hash


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__users = list()
        self.__actors = list()
        self.__movies = list()
        self.__genres = list()
        self.__directors = list()
        self.__reviews = list()

    # User
    def add_user(self, user: User):
        if type(user) == User:
            if user not in self.__users:
                self.__users.append(user)
        self.__users.sort()

    def get_user(self, user_name: str) -> User:
        for user in self.__users:
            if user.user_name == user_name.strip().lower():
                return user

    def get_user_size(self):
        return len(self.__users)

    # Actor
    def add_actor(self, actor: Actor):
        if type(actor) == Actor:
            if actor not in self.__actors:
                self.__actors.append(actor)
        self.__actors.sort()

    def get_actor(self, actor_name: str) -> Actor:
        for actor in self.__actors:
            if actor.actor_full_name == actor_name.strip():
                return actor

    def get_actor_size(self) -> int:
        return len(self.__actors)

    def get_all_actors_in_a_movie(self, movie: Movie) -> list:
        res = []
        if type(movie) == Movie:
            for actor in movie.actors:
                if actor not in res:
                    res.append(actor)
        res.sort()
        return res

    def get_all_actors(self) -> list:
        return self.__actors

    # Director
    def add_director(self, director: Director):
        if type(director) == Director:
            if director not in self.__directors:
                self.__directors.append(director)
        self.__directors.sort()

    def get_director(self, director_name: str) -> Director:
        for director in self.__directors:
            if director.director_full_name == director_name.strip():
                return director

    def get_director_size(self) -> int:
        return len(self.__directors)

    # Genre
    def add_genre(self, genre: Genre):
        if type(genre) == Genre:
            if genre not in self.__genres:
                self.__genres.append(genre)
        self.__genres.sort()

    def get_genre(self, genre_name: str) -> Genre:
        for genre in self.__genres:
            if genre.genre_name == genre_name.strip():
                return genre

    def get_genre_size(self) -> int:
        return len(self.__genres)

    # Movie
    def add_movie(self, movie: Movie):
        if type(movie) == Movie:
            if movie not in self.__movies:
                self.__movies.append(movie)
        self.__movies.sort()

    def get_movie_by_name(self, movie_name: str) -> list:
        res = []
        for movie in self.__movies:
            if movie.title == movie_name:
                res.append(movie)
        res.sort()
        return res

    def get_movie_by_year(self, release_year: int) -> list:
        res = []
        for movie in self.__movies:
            if movie.release_year == release_year:
                res.append(movie)
        res.sort()
        return res

    def get_movie_by_name_and_year(self, movie_name: str, release_year: int) -> Movie:
        for movie in self.__movies:
            if (movie.title == movie_name) and (movie.release_year == release_year):
                return movie

    def get_movie_by_actor(self, actor_name: str) -> list:
        res = []
        for movie in self.__movies:
            for actor in movie.actors:
                if actor.actor_full_name == actor_name:
                    res.append(movie)
        res.sort()
        return res

    def get_movie_by_genre(self, genre_name: str) -> list:
        res = []
        for movie in self.__movies:
            for genre in movie.genres:
                if genre.genre_name == genre_name.strip():
                    res.append(movie)
        res.sort()
        return res

    def get_movie_by_director(self, director_name: str) -> list:
        res = []
        for movie in self.__movies:
            if movie.director.director_full_name == director_name.strip():
                res.append(movie)
        res.sort()
        return res

    def get_movie_size(self) -> int:
        return len(self.__movies)

    def get_all_movies(self) -> list:
        return self.__movies


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(user_name=data_row[1], password=generate_password_hash(data_row[2]))
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_movies(data_path: str, repo: MemoryRepository):
    movies = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):
        movie = Movie(title=data_row[1].strip(), release_year=int(data_row[6]))

        actors = data_row[5]
        actors = actors.split(',')
        for actor in actors:
            actor = actor.strip()
            if Actor(actor) not in movie.actors:
                movie.add_actor(Actor(actor))

        genres = data_row[2]
        genres = genres.split(',')
        for genre in genres:
            genre = genre.strip()
            if Genre(genre) not in movie.genres:
                movie.add_genre(Genre(genre))

        director = data_row[4]
        director = director.strip()
        movie.director = Director(director)

        repo.add_movie(movie)
        movies[data_row[0]] = movie
    return movies


def populate(data_path: str, repo: MemoryRepository):
    load_movies(data_path, repo)
    load_users(data_path, repo)
