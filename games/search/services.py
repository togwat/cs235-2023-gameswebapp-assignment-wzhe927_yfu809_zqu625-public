from games.domainmodel.model import Game, Publisher, Genre
from games.adapters.repository.abstractrepo import AbstractRepository


def get_games_by_title(title: str, repo: AbstractRepository) -> list[Game]:
    if not isinstance(title, str):
        return []
    return [game for game in repo.get_games() if title.lower() in game.title.lower()]


def get_games_by_genre(genre: str, repo: AbstractRepository) -> list[Game]:
    genre = str(genre)
    games_by_genre = []
    for game in repo.get_games():
        for game_genre in game.genres:
            if genre.lower() in game_genre.genre_name.lower():
                games_by_genre.append(game)
                break
    return games_by_genre


def get_games_by_publisher(publisher: str, repo: AbstractRepository) -> list[Game]:
    if not isinstance(publisher, str):
        return []
    return [game for game in repo.get_games() if publisher.lower() in game.publisher.publisher_name.lower()]


def get_games_by_year(year: str, repo: AbstractRepository) -> list[Game]:
    # rule out rubbish input
    try:
        if 1900 > int(year) or int(year) > 3000:
            return []
    except ValueError:
        return []
    else:
        # in case argument is a reasonable integer
        year = str(year)

    games_by_year = []
    for game in repo.get_games():
        game_year = str(game.release_date.year)
        if year in game_year:
            games_by_year.append(game)
    return games_by_year


def get_game_by_id(game_id: str, repo: AbstractRepository) -> Game:
    try:
        game_id = int(game_id)
        if game_id < 0:
            return None
    except ValueError:
        return None
    else:
        return repo.get_game_by_id(game_id)
