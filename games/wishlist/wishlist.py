from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from games.authentication.services import login_required
from games.adapters.repository.abstractrepo import repo_instance as repo
import games.wishlist.services as services
wishlist_blueprint = Blueprint('wishlist_bp', __name__)

@wishlist_blueprint.route('/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist():
    game_id = request.form.get('game_id')
    username = session['username']
    user = repo.get_user(username)
    game = repo.get_game_by_id(int(game_id))

    services.add_to_wishlist(game, user, repo)

    return redirect(url_for('game_bp.home', game_id=game_id))

@wishlist_blueprint.route('/remove_from_wishlist', methods=['POST'])
@login_required
def remove_from_wishlist():
    game_id = request.form.get('game_id')
    username = session['username']
    user = repo.get_user(username)
    game = repo.get_game_by_id(int(game_id))

    services.remove_from_wishlist(game, user, repo)

    return redirect(url_for('profile_bp.profile'))
