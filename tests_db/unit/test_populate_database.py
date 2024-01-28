from sqlalchemy import select, inspect

from games.adapters.repository.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert sorted(inspector.get_table_names()) == sorted(
        ['User', 'Review', 'Game', 'Genre', 'Publisher', 'GameGenre', 'Wishlist'])


def test_database_populate_select_all_games(database_engine):
    game_table_name = 'Game'

    with database_engine.connect() as connection:
        # query for records in table 'Game'
        game_table = metadata.tables[game_table_name]
        select_statement = select(game_table)
        result = connection.execute(select_statement)

        all_game_ids = []
        for row in result:
            all_game_ids.append(row[0])

        assert 465070 in all_game_ids
        assert len(all_game_ids) == 7


def test_database_populate_select_all_genres(database_engine):
    genre_table_name = 'Genre'

    with database_engine.connect() as connection:
        # query for records in table 'Genre'
        genre_table = metadata.tables[genre_table_name]
        select_statement = select(genre_table)
        result = connection.execute(select_statement)

        all_genre_names = list()
        for row in result:
            all_genre_names.append(row[0])

        assert 'Action' in all_genre_names
