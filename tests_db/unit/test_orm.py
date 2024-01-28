import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from sqlalchemy import select, insert

from sqlalchemy.sql import text

from games.domainmodel.model import User, Game, Review, Publisher, Genre

import games.domainmodel.model

suffix = 0


def get_new_suffix() -> int:
    global suffix
    suffix += 1
    return suffix - 1


def insert_user(empty_session, user: User = None) -> str:
    """insert user record using raw sql requests. return primary key"""
    if user is None:
        user = make_user()
    username = user.username
    password = user.password

    empty_session.execute(text('INSERT INTO User (username, password) VALUES (:username, :password)'),
                          {'username': username, 'password': password})
    return username


def insert_game(empty_session, game: Game = None) -> int:
    """insert game record using raw sql requests. return primary key"""
    if game is None:
        game = make_game()
    empty_session.execute(text(
        'INSERT INTO Game (gameID, title, price, releaseDate, description, imageURL, websiteURL, publisherName) VALUES (:game_id, :title, :price, :releaseDate, :description, :imageURL, :websiteURL, :publisherName)'),
        {'game_id': game.game_id,
         'title': game.title,
         'price': game.price,
         'releaseDate': '2008-10-21',
         'description': game.description,
         'imageURL': game.image_url,
         'websiteURL': game.website_url,
         'publisherName': game.publisher.publisher_name})

    return game.game_id


def insert_genre(empty_session, genre: Genre = None) -> str:
    if genre is None:
        genre = make_genre()
    empty_session.execute(text('INSERT INTO Genre (genreName) VALUES (:genre_name)'),
                          {'genre_name': genre.genre_name})
    return genre.genre_name


def insert_publisher(empty_session, publisher: Publisher = None) -> str:
    if publisher is None:
        publisher = make_publisher()
    empty_session.execute(text('INSERT INTO Publisher (publisherName) VALUES (:publisher_name)'),
                          {'publisher_name': publisher.publisher_name})
    return publisher.publisher_name


def insert_review(empty_session, review: Review = None) -> tuple:
    if review is None:
        review = make_review()
    empty_session.execute(
        text(
            'INSERT INTO Review (username, gameID, rating, comment, timestamp) VALUES (:username, :gameID, :rating, :comment, :timestamp)'),
        {'username': review.user.username,
         'gameID': review.game.game_id,
         'rating': review.rating,
         'comment': review.comment,
         'timestamp': str(review.time)})
    return review.user.username, review.game.game_id


def insert_game_genre_association(empty_session, game: Game = None, genre: Genre = None) -> tuple:
    if game is None:
        game = make_game()
    if genre is None:
        genre = make_genre()
    empty_session.execute(text('INSERT INTO GameGenre (gameID, genreName) VALUES (:gameID, :genreName)'),
                          {'gameID': game.game_id,
                           'genreName': genre.genre_name})
    return game.game_id, genre.genre_name


def make_user(username=None, password=None) -> User:
    if username is None:
        username = f'user{get_new_suffix()}'
    if password is None:
        password = 'somepa!2Fssword'
    return User(username, password)


def make_game(game_id=None, game_title=None, publisher: Publisher = None) -> Game:
    if game_id is None:
        game_id = get_new_suffix()
    if game_title is None:
        game_title = f'game{get_new_suffix()}'
    if publisher is None:
        publisher = make_publisher()
    price = get_new_suffix()
    description = 'some description' + str(get_new_suffix())
    website_url = 'some website_url' + str(get_new_suffix())
    image_url = 'some image_url' + str(get_new_suffix())
    game = Game(game_id, game_title)
    game.price = price
    game.publisher = publisher
    game.description = description
    game.release_date = 'Oct 21, 2008'
    game.image_url = image_url
    game.website_url = website_url

    return game


def make_review(u: User = None, g: Game = None, r: int = None, c: str = None) -> Review:
    if u is None:
        u = make_user()
    if g is None:
        g = make_game()
    if r is None:
        r = 3
    if c is None:
        c = 'some comment' + str(get_new_suffix())
    return Review(user=u, game=g, rating=r, comment=c)


def make_genre(genre_name: str = None):
    if genre_name is None:
        genre_name = f'genre{get_new_suffix()}'
    return Genre(genre_name)


def make_publisher(publisher_name: str = None):
    if publisher_name is None:
        publisher_name = f'publisher{get_new_suffix()}'
    return Publisher(publisher_name)


def test_loading_of_users(empty_session):
    """write db records into db using raw sql which bypasses orm, then test retrieving python objects via orm"""
    user1 = make_user()
    user2 = make_user()
    insert_user(empty_session, user1)
    insert_user(empty_session, user2)

    assert empty_session.query(User).filter(User._User__username == user1.username).one() == user1
    assert empty_session.query(User).filter(User._User__username == user2.username).one() == user2
    assert empty_session.query(User).all() == [user1, user2]


def test_saving_of_users(empty_session):
    """save python objects to db via orm, and examine the db records"""
    # test saving distinct user
    user1 = make_user(username='username1', password='fsafE11#dd')
    user2 = make_user()
    empty_session.add(user1)
    empty_session.add(user2)
    empty_session.commit()
    rows = list(empty_session.execute(text('SELECT username, password FROM User')))
    assert rows == [(user1.username, user1.password), (user2.username, user2.password)]

    # test saving users with same username
    with pytest.raises(IntegrityError):
        user3 = make_user(username='username1', password='eggd11#d22')
        assert user1.username == user3.username
        assert user1.password != user3.password
        empty_session.add(user3)
        empty_session.commit()


def test_loading_of_games(empty_session):
    """write db records into db using raw sql which bypasses orm, then test retrieving python objects via orm"""
    game1 = make_game()
    game2 = make_game()
    insert_game(empty_session, game1)
    insert_game(empty_session, game2)
    assert empty_session.query(Game).filter(Game._Game__game_id == game1.game_id).one() == game1
    assert empty_session.query(Game).filter(Game._Game__game_id == game2.game_id).one() == game2
    assert empty_session.query(Game).all() == [game1, game2]


def test_saving_of_games(empty_session):
    """save python objects to db via orm, and examine the db records"""
    game1 = make_game()
    game2 = make_game()
    empty_session.add(game1)
    empty_session.add(game2)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT gameID FROM Game')))
    assert rows == [(game1.game_id,), (game2.game_id,)]


def test_loading_of_genres(empty_session):
    """write db records into db using raw sql which bypasses orm, then test retrieving python objects via orm"""
    genre1 = make_genre()
    genre2 = make_genre()
    insert_genre(empty_session, genre1)
    insert_genre(empty_session, genre2)
    assert empty_session.query(Genre).filter(Genre._Genre__genre_name == genre1.genre_name).one() == genre1
    assert empty_session.query(Genre).filter(Genre._Genre__genre_name == genre2.genre_name).one() == genre2
    assert empty_session.query(Genre).all() == [genre1, genre2]


def test_saving_of_genres(empty_session):
    """save python objects to db via orm, and examine the db records"""
    genre1 = make_genre()
    genre2 = make_genre()
    empty_session.add(genre1)
    empty_session.add(genre2)
    empty_session.commit()

    rows = list(empty_session.execute(text('SELECT genreName FROM Genre')))
    assert rows == [(genre1.genre_name,), (genre2.genre_name,)]


def test_loading_of_game_genre_association(empty_session):
    game1 = make_game()
    insert_game(empty_session, game1)
    genre1 = make_genre()
    insert_genre(empty_session, genre1)
    insert_game_genre_association(empty_session, game1, genre1)
    rows = list(empty_session.execute(text('SELECT * FROM GameGenre')))
    # there is to verify that the db record of the game-genre association has indeed been inserted
    assert rows == [(game1.game_id, genre1.genre_name), ]

    # now that the game, genre and their game-genre association are all in the db
    # we expect that we should be able to retrieve a game object with a 'genres' property
    retrieved_game = empty_session.query(Game).filter(Game._Game__game_id == game1.game_id).one()
    assert retrieved_game.game_id == game1.game_id
    assert genre1 in retrieved_game.genres


def test_saving_of_game_genre_association(empty_session):
    """we save a Game object that comes with a list of review into the db via orm"""
    """then we examine the GameGenre table and see if the association has been written by the orm"""
    game1 = make_game()
    genre1 = make_genre()
    game1.add_genre(genre1)
    empty_session.add(game1)
    empty_session.add(genre1)
    empty_session.commit()

    assert list(empty_session.execute(text('SELECT gameID, genreName FROM GameGenre'))) == [
        (game1.game_id, genre1.genre_name)]


def test_loading_of_review(empty_session):
    """write db records into db using raw sql which bypasses orm, then test retrieving python objects via orm"""
    user = make_user()
    game = make_game()
    review = make_review(g=game, u=user)
    game.add_review(review)
    insert_user(empty_session, user)
    insert_game(empty_session, game)
    insert_review(empty_session, review)

    # verify that the Review table has the row that we just inserted
    assert list(empty_session.execute(text('SELECT gameID, username FROM Review'))) == [(game.game_id, user.username), ]

    # change filter criteria to primary keys once the mapping to user table is fixed.
    assert empty_session.query(Review).filter(Review._Review__user == review.user).one() == review
    assert len(empty_session.query(Review).all()) == 1

    # verify that the reviews property of the Game and User Object is backpopulated
    retrieved_game = empty_session.query(Game).filter(Game._Game__game_id == game.game_id).one()
    retrieved_user = empty_session.query(User).filter(User._User__username == user.username).one()
    assert review in retrieved_game.reviews
    assert review in retrieved_user.reviews


def test_saving_of_review(empty_session):
    """save python objects to db via orm, and examine the db records"""
    user1 = make_user()
    game1 = make_game()
    empty_session.add(user1)
    empty_session.add(user1)
    empty_session.commit()

    review1 = make_review(u=user1, g=game1)
    empty_session.add(review1)
    empty_session.commit()

    # verify that the Review table is updated correctly
    rows = list(empty_session.execute(text('SELECT username, gameID FROM Review')))
    assert rows == [(review1.user.username, review1.game.game_id), ]
