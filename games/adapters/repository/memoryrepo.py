from __future__ import annotations

from games.adapters.repository.abstractrepo import AbstractRepository
from games.domainmodel.model import Genre, Game, Publisher, User, Review

from typing import List
from bisect import bisect_left, insort_left


class MemoryRepository(AbstractRepository):
    def __init__(self, genres=[], games=[], users=[], publishers=[]):
        self.__genres = genres
        self.__games = games
        self.__users = users
        self.__publishers = publishers

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and self.get_genre(genre.genre_name) is None:
            insort_left(self.__genres, genre)
            return True
        else:
            return False

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def get_genre(self, genre_name: str) -> Genre | None:
        try:
            # can binary search since sorted by username
            target_genre = Genre(genre_name)
            target_index = bisect_left(self.__genres, target_genre)
            if self.__genres[target_index] == target_genre:
                return self.__genres[target_index]
            else:
                return None
        except IndexError:
            return None


    def add_game(self, game: Game) -> bool:
        if isinstance(game, Game) and self.get_game_by_id(game.game_id) is None:
            insort_left(self.__games, game)
            return True
        else:
            return False

    def get_games(self) -> List[Game]:
        """return list of games in alphabetical order, case-insensitive"""
        return sorted(self.__games, key=lambda g: g.title.lower())

    def get_game_by_id(self, game_id: int) -> Game | None:
        try:
            # can binary search because it's id
            target_game = Game(game_id, "")
            target_index = bisect_left(self.__games, target_game)
            if self.__games[target_index] == target_game:
                return self.__games[target_index]
            else:
                return None
        except IndexError:
            return None

    def get_game_by_title(self, game_title: str) -> Game | None:
        if isinstance(game_title, str):
            # not sorted by title, has to look one by one
            for game in self.__games:
                if game.title.lower() == game_title.lower():
                    return game
        return None

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """
        Return all games with the genre in alphabetical order,
        case-insensitive
        """
        games = []

        for game in self.__games:
            if genre in game.genres:
                games.append(game)

        return sorted(games, key=lambda g: g.title.lower())

    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
        """
        Return all games with the publisher in alphabetical order,
        case-insensitive
        """
        games = []

        for game in self.__games:
            if game.publisher == publisher:
                games.append(game)

        return sorted(games, key=lambda g: g.title.lower())

    def get_number_of_games(self) -> int:
        return len(self.__games)

    def add_user(self, user: User):
        if isinstance(user, User) and self.get_user(user.username) is None:
            insort_left(self.__users, user)
            return True
        else:
            return False

    def get_user(self, username: str) -> User | None:
        try:
            # can binary search since sorted by username
            target_user = User(username, 'dummy_password')
            target_index = bisect_left(self.__users, target_user)
            if self.__users[target_index] == target_user:
                return self.__users[target_index]
            else:
                return None
        except (IndexError, ValueError):
            return None

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher) and self.get_publisher(publisher.publisher_name) is None:
            insort_left(self.__publishers, publisher)
            return True
        else:
            return False

    def get_publisher(self, publisher_name: str) -> Publisher | None:
        # binary search
        try:
            target_publisher = Publisher(publisher_name)
            target_index = bisect_left(self.__publishers, target_publisher)
            if self.__publishers[target_index] == target_publisher:
                return self.__publishers[target_index]
            else:
                return None
        except IndexError:
            return None

    def add_to_wishlist(self, user: User, game: Game):
        user.add_favourite_game(game)

    def remove_from_wishlist(self, user: User, game: Game):
        user.remove_favourite_game(game)

    def add_review(self, review: Review, user: User, game: Game):
        user.add_review(review)
        game.add_review(review)
