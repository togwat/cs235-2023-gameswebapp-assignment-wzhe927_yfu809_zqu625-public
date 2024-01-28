from games.adapters.repository.abstractrepo import AbstractRepository


def add_to_wishlist(game, user, repo: AbstractRepository):
    if game is None:
        raise GameNotFoundException
    elif user is None:
        raise UserNotFoundException
    else:
        repo.add_to_wishlist(user, game)


def remove_from_wishlist(game, user, repo: AbstractRepository):
    if user is None:
        raise UserNotFoundException
    if game is None or game not in user.favourite_games:
        raise GameNotFoundException
    else:
        repo.remove_from_wishlist(user, game)


class GameNotFoundException(Exception):
    pass


class UserNotFoundException(Exception):
    pass