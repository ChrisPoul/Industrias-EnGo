from flask import (
    Blueprint, render_template
)

bp = Blueprint('home', __name__)


@bp.route('/')
def main_page():

    return render_template(
        'home/main-page.html'
    )