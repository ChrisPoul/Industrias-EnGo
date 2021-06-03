from flask import (
    Blueprint, render_template
)
from EnGo.models.post import Post
from . import login_required

bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def main_page():
    posts = Post.get_all()

    return render_template(
        'home/main-page.html',
        posts=posts
    )