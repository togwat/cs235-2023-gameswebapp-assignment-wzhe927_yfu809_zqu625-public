import pytest
from games.adapters.repository.memoryrepo import MemoryRepository
from games.search.services import *
import random

GAME_LIST_SIZE = 100


@pytest.fixture
def new_repo(default_game_list):
    repo: AbstractRepository = MemoryRepository([], default_game_list)
    return repo


@pytest.fixture
def default_game_list():
    # game_list contains GAME_LIST_SIZE many games, each having one publisher
    # and two genres, released between 1980 and 2020
    game_list = []
    for i in range(GAME_LIST_SIZE):
        game = Game(i, f"game{i}")
        game.add_genre(Genre(f"genre{i}"))
        game.add_genre(Genre(f"genre{i % 5}"))
        game.publisher = Publisher(f"publisher{i % 5}")
        game.release_date = f"Jun {random.randint(1, 29)}, {1980 + i % 40}"
        game_list.append(game)

    return game_list


def test_get_games_by_title(new_repo):
    # test retrieving non-existent games
    assert get_games_by_title('sfhjkewjnka', new_repo) == []

    # test case sensitivity
    assert len(get_games_by_title('game1', new_repo)) == 11
    assert len(get_games_by_title('GAME1', new_repo)) == 11

    # test retrieving games by supplying partial keywords
    assert len(get_games_by_title('e1', new_repo)) > 1

    # test supplying wrong data type
    assert len(get_games_by_title(3.14, new_repo)) == 0


def test_get_games_by_publisher(new_repo):
    # test retrieving non-existent games
    assert get_games_by_publisher('fsadfwe', new_repo) == []

    # test case sensitivity
    assert len(get_games_by_publisher('publisher2', new_repo)) > 0
    assert len(get_games_by_publisher('publisher2', new_repo)) == len(get_games_by_publisher('PUBLISHER2', new_repo))

    # test retrieving games by supplying partial keywords
    assert len(get_games_by_publisher('eR3', new_repo)) > 0

    # test supplying wrong data type
    assert len(get_games_by_publisher(3.14, new_repo)) == 0


def test_get_games_by_year(new_repo):
    # test retrieving games by year
    assert len(get_games_by_year('2010', new_repo)) > 0
    assert len(get_games_by_year(2010, new_repo)) > 0

    # test supplying rubbish input
    assert len(get_games_by_year('1890', new_repo)) == 0
    assert len(get_games_by_year('foo', new_repo)) == 0
    assert len(get_games_by_year(1890, new_repo)) == 0


def test_get_game_by_id(new_repo):
    # test rubbish input
    assert get_game_by_id(-5, new_repo) is None
    assert get_game_by_id('foo', new_repo) is None

    # test valid input
    assert isinstance(get_game_by_id(15, new_repo), Game)
    assert isinstance(get_game_by_id('15', new_repo), Game)


def test_get_games_by_genre(new_repo):
    # test non-existent genres
    assert get_games_by_genre('fsadfwe', new_repo) == []

    # test case sensitivity
    assert len(get_games_by_genre('genre1', new_repo)) > 0
    assert len(get_games_by_genre('GENRE1', new_repo)) == len(get_games_by_genre('genre1', new_repo))

    # test retrieving games by supplying partial keywords
    assert len(get_games_by_genre('rE2', new_repo)) > 0

    # test supplying wrong data type
    # arguments are expected to be automatically converted into strings
    assert len(get_games_by_genre(2234234324, new_repo)) == 0
