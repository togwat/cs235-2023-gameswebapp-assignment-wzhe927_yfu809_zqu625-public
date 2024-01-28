from games.domainmodel.model import Game, Review, User
from games.adapters.repository.abstractrepo import AbstractRepository


def add_review(game: Game, user_name: str, rating: int, comment: str, repo: AbstractRepository) -> bool:
    if not isinstance(game, Game) or not isinstance(user_name, str) or not isinstance(rating, int) or not isinstance(
            comment, str):
        return False
    user = repo.get_user(user_name)
    if user is None:
        return False
    new_review = Review(user=user, game=game, rating=rating, comment=comment)
    repo.add_review(new_review, user, game)
    return True
