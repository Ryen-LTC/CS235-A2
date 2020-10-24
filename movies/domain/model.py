import csv
import datetime
from datetime import date, datetime
from typing import List, Iterable


class Actor:
    def __init__(self, actor_full_name: str):
        self.__colleague_list = []
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def add_actor_colleague(self, colleague):
        if type(colleague) == Actor:
            self.__colleague_list.append(colleague.__actor_full_name)

    def check_if_this_actor_worked_with(self, colleague):
        if type(colleague) == Actor:
            if colleague.__actor_full_name in self.__colleague_list:
                return True
            else:
                return False
        else:
            return False

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if type(other) == Actor:
            return self.__actor_full_name == other.__actor_full_name
        else:
            return False

    def __lt__(self, other):
        if type(other) == Actor:
            return self.__actor_full_name < other.__actor_full_name
        else:
            return False

    def __hash__(self):
        return hash(self.__actor_full_name)


class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if type(other) == Director:
            return self.__director_full_name == other.__director_full_name
        else:
            return False

    def __lt__(self, other):
        if type(other) == Director:
            return self.__director_full_name < other.__director_full_name
        else:
            return False

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if type(other) == Genre:
            return self.__genre_name == other.__genre_name
        else:
            return False

    def __lt__(self, other):
        if type(other) == Genre:
            return self.__genre_name < other.__genre_name
        else:
            return False

    def __hash__(self):
        return hash(self.__genre_name)


class Comment:
    def __init__(self, user: 'User', movie: 'Movie', comment: str, timestamp: datetime):
        self.__user: User = user
        self.__movie: Movie = movie
        self.__comment: Comment = comment
        self.__timestamp: datetime = timestamp

    @property
    def user(self) -> 'User':
        return self.__user

    @property
    def movie(self) -> 'Movie':
        return self.__movie

    @property
    def comment(self) -> str:
        return self.__comment

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other.__user == self.__user and other.__movie == self.__movie and other.__comment == self.__comment and other.__timestamp == self.__timestamp


class Movie:
    def __init__(self, rank: int, title: str, release_year: int, description: str):
        self.__rank = rank

        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

        if release_year < 1900 or type(release_year) is not int:
            self.__release_year = None
        else:
            self.__release_year = release_year

        self.__description = description
        self.__director = Director("")
        self.__actors = list()
        self.__genres = list()
        self.__runtime_minutes = 0
        self.__comments: List[Comment] = list()

    @property
    def comments(self) -> Iterable[Comment]:
        return iter(self.__comments)

    @property
    def number_of_comments(self) -> int:
        return len(self.__comments)

    def add_comment(self, comment: Comment):
        self.__comments.append(comment)

    @property
    def rank(self) -> int:
        return self.__rank

    # (str) this is a string with the movie title. \
    # leading and trailing whitespace has to be removed
    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new: str):
        if type(new) == str:
            self.__title = new.strip()

    @property
    def release_year(self) -> int:
        return self.__release_year

    # (str) this is a short description text of the movie. \
    # leading and trailing whitespace has to be removed
    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, new: str):
        if type(new) == str:
            self.__description = new.strip()

    # (Director) here we need one of our Director objects, \
    # there is only one director associated with a movie
    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, new: Director):
        if type(new) == Director:
            self.__director = new

    # (list of Actors) use a Python list to store one or \
    # more than one actors associated with this movie
    @property
    def actors(self) -> list:
        return self.__actors

    @actors.setter
    def actors(self, new: list):
        list1 = []
        list2 = []
        if type(new) == list and len(new) != 0:
            for actor in new:
                if type(actor) == Actor:
                    list1.append(actor)
            for actor in list1:
                if actor not in list2:
                    list2.append(actor)
            self.__actors = list2

    # (actor) adds an actor (i.e. an object instance of the class Actor) \
    # to the internal list of actors associated with this movie
    def add_actor(self, new: Actor):
        if type(new) == Actor and new not in self.__actors:
            self.__actors.append(new)

    # (actor) removes an actor from the internal list of actors. \
    # if the actor is not in the internal list, this method does nothing
    def remove_actor(self, old: Actor):
        if type(old) == Actor and old in self.__actors:
            self.__actors.remove(old)

    # (list of Genres) use a Python list to store one or more \
    # than one genres associated with this movie
    @property
    def genres(self) -> list:
        return self.__genres

    @genres.setter
    def genres(self, new: list):
        list1 = []
        list2 = []
        if type(new) == list and len(new) != 0:
            for genre in new:
                if type(genre) == Genre:
                    list1.append(genre)
            for genre in list1:
                if genre not in list2:
                    list2.append(genre)
            self.__genres = list2

    # (genre) adds a genre (i.e. an object instance of the class Genre) \
    # to the internal list of genres associated with this movie
    def add_genre(self, new: Genre):
        if type(new) == Genre and new not in self.__genres:
            self.__genres.append(new)

    # (genre) removes a genre from the internal list of genres. \
    # if the genre is not in the internal list, this method does nothing
    def remove_genre(self, old: Genre):
        if type(old) == Genre and old in self.__genres:
            self.__genres.remove(old)

    # (int) Constraint: the runtime is a positive number. \
    # A ValueError has to be raised if this constraint is not met.
    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, new: int):
        if type(new) == int and new > 0:
            self.__runtime_minutes = new
        if type(new) == int and new <= 0:
            raise ValueError

    # defines the unique string representation of the object
    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    # check for equality of two Movie object instances \
    # by comparing the titles and release years
    def __eq__(self, other):
        if type(other) == Movie:
            return (self.__title, self.__release_year) == \
                   (other.__title, other.__release_year)
        else:
            return False

    # implement a sorting order defined by the title and release year
    def __lt__(self, other):
        if type(other) == Movie:
            return (self.__title, self.__release_year) < \
                   (other.__title, other.__release_year)
        else:
            return False

    # defines which attribute is used for computing a hash \
    # value as used in set or dictionary key: remember, \
    # we uniquely define a movie through its title and release_year attributes
    def __hash__(self):
        return hash((self.__title, self.__release_year))


# used to represent user review objects.
class Review:
    # The constructor will take parameters movie, review_text \
    # and rating and will internally set a timestamp marking its creation (use Python module datetime).
    # 1. review text
    # 2. rating (which is an integer between 1 and 10), if outside this range, set to None
    # 3. timestamp indicating when the review was created
    def __init__(self, movie: Movie, review_text: str, rating: int):
        if type(movie) is not Movie:
            self.__movie = Movie("", 1899)
        else:
            self.__movie = movie

        if type(review_text) is not str or review_text == "":
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()

        if (type(rating) == int) and (1 <= rating <= 10):
            self.__rating = rating
        else:
            self.__rating = None

        self.__timestamp = datetime.datetime.today()

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    # defines the unique string representation of the object
    def __repr__(self):
        return f"<Review {self.__movie}, {self.__review_text}, {self.__rating}, {self.__timestamp}>"

    # check for equality of two Review object instances by comparing the attributes \
    # Two reviews may be considered the same, if all their attributes (including the timestamp!) are the same.
    def __eq__(self, other):
        if type(other) == Review:
            if (self.__movie == other.__movie) and (self.__review_text == other.__review_text) \
                    and (self.__rating == other.__rating) and (self.__timestamp == other.__timestamp):
                return True
            else:
                return False
        else:
            return False


# the user class stores a list of already watched movies (objects of class Movie) \
# as well as a list of reviews the user has written
class User:
    # The constructor of this class requires two string arguments, user_name and password
    def __init__(self, user_name: str, password: str):
        # (str) the user_name does not contain trailing or leading whitespace \
        # and is always converted to lowercase!
        if type(user_name) is not str or user_name == "":
            self.__user_name = None
        else:
            self.__user_name = user_name

        if type(password) is not str or password == "":
            self.__password = None
        else:
            self.__password = password

        # an integer attribute time_spent_watching_movies has to be kept up to date
        # (int) this integer is a non-negative number indicating \
        # the time already spent watching movies in the CS235Flix application
        self.__time_spent_watching_movies_minutes = 0
        self.__watched_movies = list()
        self.__reviews = list()
        self.__comments: List[Comment] = list()

    @property
    def comments(self) -> Iterable[Comment]:
        return iter(self.__comments)

    def add_comment(self, comment: Comment):
        self.__comments.append(comment)

    # (str)
    @property
    def user_name(self) -> str:
        return self.__user_name

    # (str)
    @property
    def password(self) -> str:
        return self.__password

    # (list of Movie objects)
    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    # (list of Review objects)
    @property
    def reviews(self) -> list:
        return self.__reviews

    # (int)
    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    # defines the unique string representation of the object. \
    # For a user, it will be sufficient to use the 'user_name' for this purpose.
    def __repr__(self):
        return f'<User {self.__user_name} {self.__password}>'

    # check for equality of two User object instances by comparing the user_name
    def __eq__(self, other):
        if type(other) == User:
            if self.__user_name == other.__user_name:
                return True
            else:
                return False
        else:
            return False

    # check for equality of two User object instances by comparing the names
    def __lt__(self, other):
        if type(other) == User:
            if self.__user_name < other.__user_name:
                return True
            else:
                return False
        else:
            return False

    # defines which attribute is used for computing a hash value as used in set or dictionary keys
    def __hash__(self):
        return hash(self.__user_name)

    # this method implements the action of a user watching a movie. It has to add the watched \
    # movie to the list of already watched movies, and has to update the attribute 'time_spent_watching_movies' \
    # with the runtime of the movie.
    def watch_movie(self, movie: Movie):
        if type(movie) == Movie:
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
                self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    # this method adds a review that this user has written to the list of all reviews written by this user
    def add_review(self, review: Review):
        if type(review) == Review:
            if review not in self.__reviews:
                self.__reviews.append(review)


class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    comment = Comment(user, movie, comment_text, timestamp)
    user.add_comment(comment)
    movie.add_comment(comment)

    return comment

