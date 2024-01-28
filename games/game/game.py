from flask import Blueprint, render_template, request, session, redirect, url_for

from games.authentication.services import login_required
from games.search.services import get_game_by_id
from games.game.services import add_review
from games.authentication.services import get_user
from games.adapters.repository.abstractrepo import repo_instance as repo
from games.domainmodel.model import User

game_blueprint = Blueprint('game_bp', __name__)


@game_blueprint.route('/<int:game_id>', methods=['GET'])
def home(game_id):
    current_game = get_game_by_id(game_id, repo)
    selected_review_sorting_order = request.args.get('review_sorting_order')

    reviews = []
    if selected_review_sorting_order == "most_recent" or selected_review_sorting_order is None:
        reviews = sorted(current_game.reviews, key=lambda x: x.time, reverse=True)
        selected_review_sorting_order = "most_recent"
    elif selected_review_sorting_order == "least_recent":
        reviews = sorted(current_game.reviews, key=lambda x: x.time, reverse=False)
    elif selected_review_sorting_order == "highest_rating":
        reviews = sorted(current_game.reviews, key=lambda x: x.rating, reverse=True)
    elif selected_review_sorting_order == "lowest_rating":
        reviews = sorted(current_game.reviews, key=lambda x: x.rating, reverse=False)
    elif selected_review_sorting_order == "user_name":
        reviews = sorted(current_game.reviews, key=lambda x: x.user.username, reverse=False)

    number_of_reviews = len(reviews)
    if number_of_reviews == 0:
        average_rating = 0.0
    else:
        sum_of_ratings = sum([int(r.rating) for r in reviews])
        average_rating = round(sum_of_ratings * 1.0 / number_of_reviews, 1)

    comment_status = ""
    in_wishlist = False

    try:
        user_name = session['username']
    except KeyError:
        comment_status = "user_not_logged_in"
    else:
        user = get_user(user_name)
        # repo check cuz cookie
        if user is not None:
            if user in [r.user for r in current_game.reviews]:
                comment_status = "user_has_commented"
            if current_game in user.favourite_games:
                in_wishlist = True
        else:
            comment_status = "user_not_logged_in"

    return render_template('game/game.html', current_game=current_game, reviews=reviews, average_rating=average_rating,
                           number_of_reviews=number_of_reviews,
                           number_of_stars=round(average_rating),
                           current_review_sorting_order=selected_review_sorting_order,
                           comment_status=comment_status, in_wishlist=in_wishlist)


@game_blueprint.route('/<int:game_id>', methods=['POST'])
@login_required
def comment(game_id):
    current_game = get_game_by_id(game_id, repo)
    user_name = session['username']
    data = request.form
    review_text = data['review_text']
    rating = int(data['rate'])
    add_review(current_game, user_name, rating, review_text, repo)
    return redirect(url_for('game_bp.home', game_id=game_id))
