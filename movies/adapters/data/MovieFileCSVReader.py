import csv
from movies.domain.model import Movie, Actor, Director, Genre


class MovieFileCSVReader:
    def __init__(self, file_name: str):
        self.__file_name = file_name

        # This is a list of all movies in the csv file. If you \
        # study the csv file closely you will see that these are the 1000 rows of the file.
        self.__dataset_of_movies = list()

        # This is a set of all unique actors in the csv file. An actor \
        # can be acting in more than one movie, so we have to be careful during reading!
        self.__dataset_of_actors = list()

        # This is a set of all unique directors in the csv file. \
        # A director can direct more than one movie, so we have to be careful during reading!
        self.__dataset_of_directors = list()

        # This is a set of all unique genres in the csv file. A genre can \
        # be associated with many movies, and there are only a small number of unique genres in the csv file.
        self.__dataset_of_genres = list()

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csv_file:
            movie_file_reader = csv.DictReader(csv_file)

            list_movies = []
            list_actors = []
            list_directors = []
            list_genres = []
            for row in movie_file_reader:

                # unique movies
                title = row['Title']
                title = title.strip()
                release_year = int(row['Year'])
                if Movie(title, release_year) not in list_movies:
                    list_movies.append(Movie(title, release_year))

                # unique actors
                actors = row['Actors']
                actors = actors.split(',')
                for actor in actors:
                    actor = actor.strip()
                    if Actor(actor) not in list_actors:
                        list_actors.append(Actor(actor))

                # unique directors
                directors = row['Director']
                directors = directors.split(',')
                for director in directors:
                    director = director.strip()
                    if Director(director) not in list_directors:
                        list_directors.append(Director(director))

                # unique genres
                genres = row['Genre']
                genres = genres.split(',')
                for genre in genres:
                    genre = genre.strip()
                    if Genre(genre) not in list_genres:
                        list_genres.append(Genre(genre))

            self.__dataset_of_movies = list_movies
            self.__dataset_of_actors = list_actors
            self.__dataset_of_directors = list_directors
            self.__dataset_of_genres = list_genres

    @property
    def dataset_of_movies(self) -> list:
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self) -> list:
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self) -> list:
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self) -> list:
        return self.__dataset_of_genres

