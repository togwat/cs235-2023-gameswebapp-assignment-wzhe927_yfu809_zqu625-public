from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Text, Numeric, SMALLINT,
    ForeignKey, PrimaryKeyConstraint, Table, MetaData
)
from sqlalchemy.orm import registry, relationship
from games.domainmodel.model import Publisher, Genre, Game, User, Review

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

genre_table = Table(
    'Genre', metadata,
    Column('genreName', String(64), primary_key=True)
)

publisher_table = Table(
    'Publisher', metadata,
    Column('publisherName', String(64), primary_key=True)
)

game_table = Table(
    'Game', metadata,
    Column('gameID', Integer, primary_key=True, autoincrement=True),
    Column('title', String(128), nullable=False),
    Column('price', Numeric(10, 2), nullable=False),    # 10 digits, 2 are decimals
    Column('releaseDate', Date, nullable=False),
    Column('description', Text, nullable=True),
    Column('imageURL', String(255), nullable=True),
    Column('websiteURL', String(255), nullable=True),
    Column('publisherName', ForeignKey('Publisher.publisherName'))
)

game_genre_table = Table(
    'GameGenre', metadata,
    Column('gameID', Integer, ForeignKey('Game.gameID')),
    Column('genreName', String(64), ForeignKey('Genre.genreName')),
    PrimaryKeyConstraint('gameID', 'genreName')
)

user_table = Table(
    'User', metadata,
    Column('username', String(64), primary_key=True),
    Column('password', String(64), nullable=False),   # sha256 hash
)

review_table = Table(
    'Review', metadata,
    Column('username', String(64), ForeignKey('User.username')),
    Column('gameID', Integer, ForeignKey('Game.gameID')),
    Column('rating', SMALLINT, nullable=False),
    Column('comment', Text, nullable=True),
    Column('timestamp', DateTime, nullable=False),
    PrimaryKeyConstraint('username', 'gameID')
)

wishlist_table = Table(
    'Wishlist', metadata,
    Column('username', String(64), ForeignKey('User.username')),
    Column('gameID', Integer, ForeignKey('Game.gameID')),
    PrimaryKeyConstraint('username', 'gameID')
)


def map_model_to_tables():
    mapper_registry.map_imperatively(Genre, genre_table, properties={
        '_Genre__genre_name': genre_table.c.genreName
    })

    mapper_registry.map_imperatively(Publisher, publisher_table, properties={
        '_Publisher__publisher_name': publisher_table.c.publisherName
    })

    mapper_registry.map_imperatively(Game, game_table, properties={
        '_Game__game_id': game_table.c.gameID,
        '_Game__game_title': game_table.c.title,
        '_Game__price': game_table.c.price,
        '_Game__release_date': game_table.c.releaseDate,
        '_Game__description': game_table.c.description,
        '_Game__image_url': game_table.c.imageURL,
        '_Game__website_url': game_table.c.websiteURL,
        '_Game__publisher': relationship(Publisher, lazy='subquery'),
        '_Game__genres': relationship(Genre, secondary=game_genre_table, lazy='subquery'),
        '_Game__reviews': relationship(Review, back_populates='_Review__game')
    })

    mapper_registry.map_imperatively(User, user_table, properties={
        '_User__username': user_table.c.username,
        '_User__password': user_table.c.password,
        '_User__reviews': relationship(Review, back_populates='_Review__user'),
        '_User__favourite_games': relationship(Game, secondary=wishlist_table)
    })

    mapper_registry.map_imperatively(Review, review_table, properties={
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__game': relationship(Game, back_populates='_Game__reviews'),
        '_Review__rating': review_table.c.rating,
        '_Review__comment': review_table.c.comment,
        '_Review__time': review_table.c.timestamp
    })

    # mapper_registry.map_imperatively(Wishlist, wishlist_table, properties={
    #     # '_Wishlist__user': relationship(User, back_populates='_User__favourite_games'),
    #     '_Wishlist__list_of_games': relationship(Game)
    # })
