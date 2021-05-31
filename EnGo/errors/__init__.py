from flask import (
    Blueprint, render_template
)

bp = Blueprint("error", __name__)


@bp.app_errorhandler(404)
def error_404(error):
    return render_template("error/404.html"), 404
