import pytest
from games.domainmodel.model import Publisher, Genre, Game, User
from games.adapters.repository.abstractrepo import populate
from os.path import exists, join, dirname, abspath


def test_add_genre_and_get_genre(empty_repo):
    # test empty repo
    assert empty_repo.get_genres() == []

    # test garbage inputs
    assert empty_repo.add_genre("haha") is False
    assert empty_repo.add_genre(123) is False
    assert empty_repo.get_genres() == []

    # test valid inputs
    assert empty_repo.add_genre(Genre("Genre1")) is True
    assert empty_repo.get_genres() == [Genre("Genre1"), ]
    assert empty_repo.add_genre(Genre("Genre2")) is True
    assert empty_repo.get_genres() == [Genre("Genre1"), Genre("Genre2"), ]

    # test duplicate genres
    assert empty_repo.add_genre(Genre("Genre1")) is False
    assert empty_repo.get_genres() == [Genre("Genre1"), Genre("Genre2"), ]


def test_add_game_and_get_games(empty_repo):
    # test get_games with empty repo
    assert empty_repo.get_games() == []
    assert len(empty_repo.get_games()) == 0

    # test adding two identical game objects
    assert empty_repo.add_game(Game(1, 'foo')) is True
    assert len(empty_repo.get_games()) == 1
    assert empty_repo.add_game(Game(1, 'foo')) is False
    assert len(empty_repo.get_games()) == 1

    # test adding two game objects with same id
    assert empty_repo.add_game(Game(1, 'bar')) is False
    assert len(empty_repo.get_games()) == 1

    # test adding items of wrong type
    assert empty_repo.add_game('new game') is False
    assert len(empty_repo.get_games()) == 1

    # test adding a new game object
    assert empty_repo.add_game(Game(2, 'bar')) is True
    assert len(empty_repo.get_games()) == 2

    # test get_games with non-empty repo
    assert sorted(empty_repo.get_games()) == sorted([Game(1, 'foo'), Game(2, 'bar')])


def test_get_game_by_id(empty_repo):
    empty_repo.add_game(Game(1, 'foo'))
    empty_repo.add_game(Game(2, 'bar'))

    # test retrieving an existing game object
    assert empty_repo.get_game_by_id(1) == Game(1, 'foo')

    # test retrieving a non-existent game object
    assert empty_repo.get_game_by_id(3) is None

    # test passing wrong date type
    with pytest.raises(ValueError):
        empty_repo.get_game_by_id('foo')

    # test passing negative value
    with pytest.raises(ValueError):
        empty_repo.get_game_by_id(-100)


def test_get_game_by_title(empty_repo):
    empty_repo.add_game(Game(1, 'foo'))
    empty_repo.add_game(Game(2, 'bar'))

    # test retrieving existing and non-existent games by title
    assert empty_repo.get_game_by_title('foo') == Game(1, 'foo')
    assert empty_repo.get_game_by_title('baz') is None

    # test case sensitivity
    assert empty_repo.get_game_by_title('FOO') == Game(1, 'foo')

    # test passing wrong data type
    # the implementation returns None instead of raising an error which is fine
    assert empty_repo.get_game_by_title(1) is None


def test_get_games_by_genre(empty_repo):
    game1 = Game(1, 'foo')
    game2 = Game(2, 'bar')
    game3 = Game(3, 'baz')

    game1.add_genre(Genre('action'))
    game2.add_genre(Genre('action'))
    game3.add_genre((Genre('FPS')))

    empty_repo.add_game(game1)
    empty_repo.add_game(game2)
    empty_repo.add_game(game3)

    # test non-existent genres
    assert empty_repo.get_games_by_genre((Genre('sadfew'))) == []

    # test existing genres
    assert sorted(empty_repo.get_games_by_genre(Genre('action'))) == sorted([game1, game2])
    assert sorted(empty_repo.get_games_by_genre(Genre('FPS'))) == sorted([game3, ])


def test_get_games_by_publisher(empty_repo):
    game1 = Game(1, 'foo')
    game2 = Game(2, 'bar')
    game3 = Game(3, 'baz')

    game1.publisher = Publisher('EA Games')
    game2.publisher = Publisher('EA Games')
    game3.publisher = Publisher('Rockstar')

    empty_repo.add_game(game1)
    empty_repo.add_game(game2)
    empty_repo.add_game(game3)

    # test non-existent publishers
    assert sorted(empty_repo.get_games_by_publisher(Publisher('2K Games'))) == sorted([])

    # test existing publishers
    assert sorted(empty_repo.get_games_by_publisher(Publisher('EA Games'))) == sorted([game1, game2])
    assert sorted(empty_repo.get_games_by_publisher(Publisher('Rockstar'))) == sorted([game3, ])


def test_get_number_of_games(empty_repo):
    # test empty repo
    assert empty_repo.get_number_of_games() == 0

    empty_repo.add_game(Game(1, 'foo'))
    empty_repo.add_game(Game(2, 'bar'))

    # test non-empty repo
    assert empty_repo.get_number_of_games() == 2


def test_add_user_and_get_user(empty_repo):
    # test garbage inputs
    assert empty_repo.get_user(123) is None
    assert empty_repo.add_user(123) is False

    # test valid inputs
    assert empty_repo.add_user(User(username="James", password="123456Abc!")) is True
    assert empty_repo.get_user("James") == User(username="James", password="123456Abc!")

    # test duplicate inputs
    assert empty_repo.add_user(User(username="James", password="123456Abc!")) is False
    assert empty_repo.get_user("James") == User(username="James", password="123456Abc!")


def test_add_publisher_and_get_publisher(empty_repo):
    # test garbage inputs
    assert empty_repo.add_publisher("") is False
    assert empty_repo.add_publisher(123) is False

    # test valid inputs
    assert empty_repo.add_genre(Genre("paradox")) is True
    assert empty_repo.get_genres() == [Genre("paradox"), ]
    assert empty_repo.add_genre(Genre("rock and stone")) is True
    assert empty_repo.get_genres() == [Genre("paradox"), Genre("rock and stone"), ]

    # test duplicate genres
    assert empty_repo.add_genre(Genre("paradox")) is False
    assert empty_repo.get_genres() == [Genre("paradox"), Genre("rock and stone"), ]


def test_populate(empty_repo):
    # test empty repo
    assert empty_repo.get_number_of_games() == 0

    # keep going up one directory until the source data file is found
    current_directory = dirname(abspath(__file__))
    directory_depth = 1
    while True:
        source_data_path = join(current_directory, 'games/adapters/data/games.csv')
        if exists(source_data_path):
            break
        else:
            current_directory = dirname(current_directory)
            assert directory_depth < 5  # in case of failing to find the csv file
            directory_depth += 1

    populate(source_data_path, empty_repo)

    # test repo filled with imported data
    assert empty_repo.get_number_of_games() > 500
