from flask import Blueprint, render_template, redirect, url_for, request
from games.pagination.pagination import Pagination
from games.pagination.services import create_pagination_list
import games.adapters.repository.abstractrepo as repo

genre_sidebar_blueprint = Blueprint('genre_sidebar_bp', __name__)
all_games = repo.repo_instance.get_games()

@genre_sidebar_blueprint.route('/genre')
def genre():
    return redirect(url_for('genre_sidebar_bp.go_to_page', page_num=1, **request.args))


@genre_sidebar_blueprint.route('/genre/<int:page_num>')
def go_to_page(page_num):
    genre_name = request.args.get('genre_name')
    games = [game for game in all_games if genre_name in [genre.genre_name for genre in game.genres]]
    # paginate game list and return the specified page
    pagination = Pagination(games)
    pagination.go_to_page(page_num)
    page_content = pagination.get_page_content()

    # if there are 5 pages, pagination_list will be [1, 2, 3, 4, 5]
    # if more than 7 pages, then [1, 2, 3, 4, 5, 6, 7]
    pages = create_pagination_list(pagination.current_page, pagination.page_count)
    return render_template('genre_library/genre_library.html',
                           games=page_content, genre_name=genre_name, page_list=pages,
                           page_num=pagination.current_page, page_count=pagination.page_count)