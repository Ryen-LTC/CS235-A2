from flask import Blueprint, render_template
from movies.domain.model import Movie

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home/home.html')

