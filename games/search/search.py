from games.pagination.pagination import Pagination
from games.pagination.services import create_pagination_list
from flask import Blueprint, render_template, request, redirect, url_for
from games.adapters.repository.abstractrepo import repo_instance as repo
from games.search.services import *

search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search/', methods=['GET'])
def search_results():
    return redirect(url_for('search_bp.go_to_page', page_num=1,
                            **request.args))


@search_blueprint.route('/search/<page_num>', methods=['GET'])
def go_to_page(page_num):
    # obtain query parameters
    term = request.args.get('term')
    criteria = request.args.get('criteria')

    # generate a list of eligible games
    if criteria == 'title':
        games = get_games_by_title(term, repo)
    elif criteria == 'publisher':
        games = get_games_by_publisher(term, repo)
    elif criteria == 'year':
        games = get_games_by_year(term, repo)
    elif criteria == 'genre':
        games = get_games_by_genre(term, repo)
    else:
        games = []

    # paginate game list and return the specified page
    pagination = Pagination(games)
    pagination.go_to_page(int(page_num))
    page_content = pagination.get_page_content()

    # if there are 5 pages, pagination_list will be [1, 2, 3, 4, 5]
    # if more than 7 pages, then [1, 2, 3, 4, 5, 6, 7]
    pages = create_pagination_list(pagination.current_page,
                                   pagination.page_count)

    return render_template('/search/searchResult.html',
                           games=page_content,
                           page_list=pages,
                           page_num=pagination.current_page,
                           page_count=pagination.page_count, **request.args,
                           )
