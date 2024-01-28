"""Initialize Flask app."""

from flask import Flask

import games.adapters.repository.abstractrepo as repo
import games.adapters.repository.databaserepo
from games.adapters.repository.memoryrepo import MemoryRepository
from games.adapters.repository.databaserepo import DatabaseRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from os.path import exists, join, dirname, abspath

from games.context_processors import sidebar_context

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from games.adapters.repository.orm import map_model_to_tables, metadata

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    if test_config is not None:
        app.config.update(test_config)

    # prevents repeating sidebar stuff in view functions
    app.context_processor(sidebar_context)

    # .env variables from config
    app.config.from_object('config.Config')

    # locate the data source file
    current_directory = dirname(abspath(__file__))
    directory_depth = 1
    while True:
        data_source_path = join(current_directory, 'games/adapters/data/games.csv')
        if exists(data_source_path):
            break
        else:
            current_directory = dirname(current_directory)
            if directory_depth > 5:
                print("Failed to locate games/adapters/data/games.csv")
                exit()
            directory_depth += 1

    if app.config['REPOSITORY'] == 'memory':
        # create memory repository
        repo.repo_instance = MemoryRepository()

        # import game data from source into repo
        repo.populate(data_source_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=database_echo)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        repo.repo_instance = DatabaseRepository(session_factory)

        # run without database instance
        if len(inspect(database_engine).get_table_names()) == 0 or app.config['TESTING'] == 'True':
            print('REPOPULATING DATABASE')
            clear_mappers()
            metadata.create_all(database_engine)
            # clear data
            for table in reversed(metadata.sorted_tables):
                with database_engine.connect() as connection:
                    connection.execute(table.delete())

            map_model_to_tables()
            repo.populate(data_source_path, repo.repo_instance)
            print('REPOPULATING DATABASE... FINISHED')

        else:
            map_model_to_tables()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .library import library
        app.register_blueprint(library.library_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from games.game.game import game_blueprint
        app.register_blueprint(game_blueprint, url_prefix='/game')

        from .genre_sidebar.genre_sidebar import genre_sidebar_blueprint
        app.register_blueprint(genre_sidebar_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .wishlist import wishlist
        app.register_blueprint(wishlist.wishlist_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, games.adapters.repository.databaserepo.DatabaseRepository):
                repo.repo_instance.reset_session()

        @app.teardown_request
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, games.adapters.repository.databaserepo.DatabaseRepository):
                repo.repo_instance.close_session()

    return app
