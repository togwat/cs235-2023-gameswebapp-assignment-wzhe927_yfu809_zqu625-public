from flask import Blueprint, render_template, redirect, url_for, session
from games.authentication.services import login_required
from games.adapters.repository.abstractrepo import repo_instance as repo



profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile')
@login_required
def profile():
    username = session['username']
    user = repo.get_user(username)
    reviews = user.reviews
    wishlist_games = user.favourite_games
    return render_template('profile/profile.html', current_page='profile', reviews=reviews, wishlist_games=wishlist_games)


@profile_blueprint.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('authentication_bp.login'))
