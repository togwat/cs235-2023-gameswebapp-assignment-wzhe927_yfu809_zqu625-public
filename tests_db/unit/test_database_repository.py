from games.adapters.repository.databaserepo import DatabaseRepository
from tests_db.unit.test_orm import make_game, make_user, make_genre, make_review, make_publisher


def test_add_and_get_user(session_factory):
    repo = DatabaseRepository(session_factory)
    user = make_user()
    repo.add_user(user)

    # test getting user
    user2 = repo.get_user(user.username)
    assert user2 == user

    # test getting non-existent user
    assert repo.get_user('some user') is None

def test_get_and_add_genre(session_factory):
    repo = DatabaseRepository(session_factory)
    genre1 = make_genre()
    repo.add_genre(genre1)

    # test getting genre by name
    assert repo.get_genre(genre1.genre_name) == genre1

    # test getting non-existent genre
    assert repo.get_genre('some genre') is None

    # test getting all genres
    assert len(repo.get_genres()) > 5
    assert genre1 in repo.get_genres()

def test_add_game_and_get_game(session_factory):
    repo = DatabaseRepository(session_factory)
    publisher1 = make_publisher()
    publisher2 = make_publisher()
    genre1 = make_genre()
    genre2 = make_genre()

    game1 = make_game(publisher=publisher1)
    game2 = make_game(publisher=publisher1)
    game3 = make_game(publisher=publisher2)

    game1.add_genre(genre1)
    game2.add_genre(genre1)
    game2.add_genre(genre2)
    game3.add_genre(genre2)

    repo.add_game(game1)
    repo.add_game(game2)
    repo.add_game(game3)

    # test add_game and retrieving single game by id
    assert repo.get_game_by_id(game1.game_id) == game1

    # test retrieving single game by title, lower and upper cases
    assert repo.get_game_by_title(game2.title.lower()) == game2
    assert repo.get_game_by_title(game2.title.upper()) == game2

    # test getting number of games and getting all games
    assert repo.get_number_of_games() > 500
    assert repo.get_number_of_games() == len(repo.get_games())


def test_add_review(session_factory):
    repo = DatabaseRepository(session_factory)
    user = make_user()
    repo.add_user(user)
    game = make_game()
    repo.add_game(game)

    review = make_review(user, game)
    repo.add_review(review, user, game)
    assert review in game.reviews
    assert review in user.reviews
