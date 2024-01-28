import games.adapters.repository.abstractrepo as repo
from flask import session


def sidebar_context():
    """Common sidebar parameter items that are repeated"""
    genres = repo.repo_instance.get_genres()
    username = 'Login'  # default value for profile tab is login
    if 'username' in session:
        username = session['username']

    return {
        'genres': genres,
        'username': username
    }
