from flask import (
    Blueprint, render_template
)
from . import permission_required, login_required

bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def main_page():

    return render_template(
        'home/main-page.html'
    )