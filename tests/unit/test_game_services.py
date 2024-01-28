import pytest

from games.domainmodel.model import Game, User
from games.game.services import add_review
from games.wishlist.services import add_to_wishlist, remove_from_wishlist, GameNotFoundException, UserNotFoundException
from games.adapters.repository.memoryrepo import MemoryRepository


def test_add_review(empty_repo):
    game1 = Game(1, "game1")
    user_name = "user1"
    user1 = User(user_name, "password1")
    rating = 3
    comment = "good"

    empty_repo.add_game(game1)
    empty_repo.add_user(user1)

    # test invalid arguments
    assert add_review(123, user_name, rating, comment, empty_repo) is False
    assert add_review(game1, 123, rating, comment, empty_repo) is False
    assert add_review(game1, user_name, "haha", comment, empty_repo) is False
    assert add_review(game1, user_name, rating, 123, empty_repo) is False

    # test non-existent user
    assert add_review(game1, "user2", rating, comment, empty_repo) is False

    # test valid input
    assert add_review(game1, user_name, rating, comment, empty_repo) is True


def test_wishlist(empty_repo):
    game1 = Game(1, "game1")
    game2 = Game(2, "game2")
    game3 = Game(3, "game3")
    user = User('user', 'dummypassword')

    empty_repo.add_game(game1)
    empty_repo.add_game(game2)
    empty_repo.add_game(game3)
    empty_repo.add_user(user)

    # add wishlist
    expected_wishlist = [game1]
    add_to_wishlist(game1, user, empty_repo)
    assert user.favourite_games == expected_wishlist

    expected_wishlist = [game1, game2]
    add_to_wishlist(game2, user, empty_repo)
    assert user.favourite_games == expected_wishlist

    # no game
    with pytest.raises(GameNotFoundException):
        add_to_wishlist(empty_repo.get_game_by_title('gameNone'), user, empty_repo)

    # no user
    with pytest.raises(UserNotFoundException):
        add_to_wishlist(game3, empty_repo.get_user('userNone'), empty_repo)

    expected_wishlist = [game1, game2, game3]
    add_to_wishlist(game3, user, empty_repo)
    assert user.favourite_games == expected_wishlist

    # remove games
    expected_wishlist = [game1, game2]
    remove_from_wishlist(game3, user, empty_repo)
    assert user.favourite_games == expected_wishlist

    expected_wishlist = [game2]
    remove_from_wishlist(game1, user, empty_repo)
    assert user.favourite_games == expected_wishlist

    # no game
    with pytest.raises(GameNotFoundException):
        remove_from_wishlist(game3, user, empty_repo)
    with pytest.raises(GameNotFoundException):
        remove_from_wishlist(empty_repo.get_game_by_title('gameNone'), user, empty_repo)

    # no user
    with pytest.raises(UserNotFoundException):
        remove_from_wishlist(game2, empty_repo.get_user('userNone'), empty_repo)

    # empty
    expected_wishlist = []
    remove_from_wishlist(game2, user, empty_repo)
    assert user.favourite_games == expected_wishlist

    with pytest.raises(GameNotFoundException):
        remove_from_wishlist(game1, user, empty_repo)



