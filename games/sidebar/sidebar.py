from flask import Blueprint, render_template
from games.adapters.datareader.csvdatareader import GameFileCSVReader

sidebar_blueprint = Blueprint('sidebar_bp', __name__)
reader = GameFileCSVReader("games/adapters/data/games.csv")
reader.read_csv_file()
list_of_genres = reader.dataset_of_genres

@sidebar_blueprint.route('/sidebar')
def sidebar():
    return render_template('sidebar/sidebar.html', genres=list_of_genres)
