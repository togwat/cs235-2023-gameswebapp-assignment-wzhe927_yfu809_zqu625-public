import math

import pytest
from games.domainmodel.model import Publisher, Genre, Game
from games.pagination.pagination import Pagination
from games.pagination.services import create_pagination_list

GAME_LIST_SIZE = 100


@pytest.fixture
def default_game_list():
    game_list = []
    for i in range(GAME_LIST_SIZE):
        game = Game(i, f"game{i}")
        game_list.append(game)
    return game_list


@pytest.fixture
def new_pagination(default_game_list):
    return Pagination(games=default_game_list)


@pytest.fixture
def new_empty_pagination():
    return Pagination(games=[])


def test_page_count(new_pagination, new_empty_pagination):
    # test pagination object with empty game list
    assert new_empty_pagination.page_count == 0

    # test pagination object with non-empty game list
    page_count = math.ceil(float(GAME_LIST_SIZE) / Pagination.PAGE_SIZE)
    assert new_pagination.page_count == page_count


def test_go_to_page(new_pagination, new_empty_pagination):
    # test default current page
    assert new_empty_pagination.current_page == 1
    assert new_pagination.current_page == 1

    # normal page numbers
    new_pagination.go_to_page(10)
    assert new_pagination.current_page == 10

    # page_num overflow. out of range page_num is expected to be ignored
    assert new_pagination.current_page == 10
    new_pagination.go_to_page(new_pagination.page_count + 1234)
    assert new_pagination.current_page == 10

    # page_num underflow. out of range page_num is expected to be ignored
    assert new_pagination.current_page == 10
    new_pagination.go_to_page(-1234)
    assert new_pagination.current_page == 10
    new_pagination.go_to_page(0)
    assert new_pagination.current_page == 10


def test_create_pagination_list():
    # normal page numbers
    assert create_pagination_list(page_num=1, total_pages=1) == [1, ]
    assert create_pagination_list(page_num=1, total_pages=3) == [1, 2, 3]
    assert create_pagination_list(page_num=2, total_pages=3) == [1, 2, 3]
    assert create_pagination_list(page_num=3, total_pages=3) == [1, 2, 3]
    assert create_pagination_list(page_num=1, total_pages=7) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=5, total_pages=7) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=7, total_pages=7) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=1, total_pages=9) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=5, total_pages=9) == [2, 3, 4, 5, 6, 7, 8]
    assert create_pagination_list(page_num=9, total_pages=9) == [3, 4, 5, 6, 7, 8, 9]

    # page_num overflow
    assert create_pagination_list(page_num=1234, total_pages=1) == [1, ]
    assert create_pagination_list(page_num=1234, total_pages=3) == [1, 2, 3]
    assert create_pagination_list(page_num=1234, total_pages=7) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=1234, total_pages=8) == [2, 3, 4, 5, 6, 7, 8]

    # page_num underflow
    assert create_pagination_list(page_num=0, total_pages=1) == [1, ]
    assert create_pagination_list(page_num=0, total_pages=3) == [1, 2, 3]
    assert create_pagination_list(page_num=0, total_pages=7) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=0, total_pages=100) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=-1234, total_pages=1) == [1, ]
    assert create_pagination_list(page_num=-1234, total_pages=3) == [1, 2, 3]
    assert create_pagination_list(page_num=-1234, total_pages=7) == [1, 2, 3, 4, 5, 6, 7]
    assert create_pagination_list(page_num=-1234, total_pages=100) == [1, 2, 3, 4, 5, 6, 7]


def test_get_page_content(new_pagination, new_empty_pagination, default_game_list):
    # empty pagination
    assert new_empty_pagination.get_page_content() == []

    # test getting page content with current page == 1
    assert new_pagination.current_page == 1
    assert new_pagination.get_page_content() == default_game_list[0:Pagination.PAGE_SIZE]

    # test getting page content with current page == 2
    assert new_pagination.page_count > 2
    new_pagination.go_to_page(2)
    assert new_pagination.current_page == 2
    assert new_pagination.get_page_content() == default_game_list[(
                                                                          new_pagination.current_page - 1) * Pagination.PAGE_SIZE:new_pagination.current_page * Pagination.PAGE_SIZE]

    # set up game_list for further tests
    game_list = [Game(1, "game1"),
                 Game(2, "game2"),
                 Game(3, "game3"),
                 Game(4, "game4"),
                 Game(5, "game5"),
                 Game(6, "game6"),
                 Game(7, "game7"),
                 Game(8, "game8")]
    my_pagination = Pagination(games=game_list)
    assert Pagination.PAGE_SIZE == 6
    assert my_pagination.page_count == 2

    # test getting page content from last page
    # there are 8 items while each page can contain 6, so the last page is expected to have 2 items
    my_pagination.go_to_page(2)
    assert my_pagination.current_page == 2
    assert my_pagination.get_page_content() == [Game(7, "game7"), Game(8, "game8")]
