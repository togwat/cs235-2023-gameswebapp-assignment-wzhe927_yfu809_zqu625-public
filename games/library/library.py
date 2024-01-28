from flask import Blueprint, render_template, redirect, url_for
import games.adapters.repository.abstractrepo as repo
from games.pagination.pagination import Pagination
from games.pagination.services import create_pagination_list

library_blueprint = Blueprint('library_bp', __name__)

games = repo.repo_instance.get_games()
# pagination
pagination = Pagination(games)


# doubles as go to first page function
@library_blueprint.route('/library/')
def library():
    return redirect(url_for('library_bp.go_to_page', page_num=1))


@library_blueprint.route('/library/<page_num>')
def go_to_page(page_num):
    pagination.go_to_page(int(page_num))
    page_content = pagination.get_page_content()
    pages = create_pagination_list(pagination.current_page,
                                   pagination.page_count)

    return render_template('library/library.html',
                           current_page='library',
                           games=page_content,
                           page_num=pagination.current_page,
                           page_list=pages,
                           page_count=pagination.page_count,
                           )
