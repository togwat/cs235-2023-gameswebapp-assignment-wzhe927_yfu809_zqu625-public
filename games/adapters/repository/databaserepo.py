from __future__ import annotations

from sqlalchemy import func

from games.adapters.repository.abstractrepo import AbstractRepository
from games.domainmodel.model import Genre, Game, Publisher, User, Review
from typing import List

from sqlalchemy.orm import scoped_session


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class DatabaseRepository(AbstractRepository):
    def __init__(self, session_factory):
        self.__scm = SessionContextManager(session_factory)

    def close_session(self):
        self.__scm.close_current_session()

    def reset_session(self):
        self.__scm.reset_session()

    def add_genre(self, genre: Genre):
        with self.__scm as scm:
            scm.session.merge(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        genres = self.__scm.session.query(Genre).all()
        return genres

    def get_genre(self, genre_name: str) -> Genre | None:
        genre = self.__scm.session.query(Genre).filter(func.lower(Genre._Genre__genre_name) == genre_name.lower()).first()
        return genre

    def add_game(self, game: Game):
        with self.__scm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_publisher(self, publisher: Publisher):
        with self.__scm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def get_publisher(self, publisher_name: str) -> Publisher | None:
        publisher = self.__scm.session.query(Publisher).filter(func.lower(Publisher._Publisher__publisher_name) == publisher_name.lower()).first()
        return publisher

    def get_games(self) -> List[Game]:
        games = self.__scm.session.query(Game).all()
        return games

    def get_game_by_id(self, game_id: int) -> Game | None:
        game = self.__scm.session.query(Game).filter(Game._Game__game_id == game_id).first()
        return game

    def get_game_by_title(self, game_title: str) -> Game | None:
        game = self.__scm.session.query(Game).filter(func.lower(Game._Game__game_title) == game_title.lower()).first()
        return game

    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        games = self.__scm.session.query(Game).filter(Game._Game__genres.contains(genre)).all()
        return games

    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
        games = self.__scm.session.query(Game).filter(Game.publisher == publisher).all()
        return games

    def get_number_of_games(self) -> int:
        return self.__scm.session.query(Game).count()

    def add_user(self, user: User):
        with self.__scm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, username: str) -> User | None:
        user = self.__scm.session.query(User).filter(func.lower(User._User__username) == username.lower()).first()
        return user

    def add_to_wishlist(self, user: User, game: Game):
        with self.__scm as scm:
            user.add_favourite_game(game)
            scm.commit()

    def remove_from_wishlist(self, user: User, game: Game):
        with self.__scm as scm:
            user.remove_favourite_game(game)
            scm.commit()

    def add_review(self, review: Review, user: User, game: Game):
        with self.__scm as scm:
            user.add_review(review)
            game.add_review(review)
            scm.commit()
