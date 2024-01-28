import abc
from games.domainmodel.model import Genre, Game, Publisher, User, Review
from typing import List
from games.adapters.datareader.csvdatareader import GameFileCSVReader


repo_instance = None


class AbstractRepository(abc.ABC):
    # storing
    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, game: Publisher):
        raise NotImplementedError

    # retrieving
    @abc.abstractmethod
    def get_publisher(self, publisher_name: str) -> Publisher:
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    def get_genre(self, genre_name: str) -> Genre:
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_id(self, game_id: int) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_by_title(self, game_title: str) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """
        returns all games with the genre, ordered alphabetically
        returns empty list if genre doesn't have any games
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
        """
        returns all games with the publisher, ordered alphabetically
        returns empty list if publisher doesn't have any games
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """Add new user to a list of users"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """Returns user with matching username, or none"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_to_wishlist(self, user: User, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def remove_from_wishlist(self, user: User, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review, user: User, game: Game):
        raise NotImplementedError


def populate(path, repo: AbstractRepository):
    reader = GameFileCSVReader(path)
    reader.read_csv_file()

    games = reader.dataset_of_games
    for game in games:
        repo.add_game(game)

    genres = reader.dataset_of_genres
    for genre in genres:
        repo.add_genre(genre)

    publishers = reader.dataset_of_publishers
    for publisher in publishers:
        repo.add_publisher(publisher)
