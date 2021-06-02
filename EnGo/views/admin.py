from flask import (
    Blueprint, render_template, request,
    redirect, url_for
)
from . import permission_required, login_required
from .user import username_head
from EnGo.models.user import User
from EnGo.models.view import View

bp = Blueprint('admin', __name__, url_prefix="/admin")

@bp.route("/main_page", methods=('POST', 'GET'))
@permission_required(["Admin"])
@login_required
def main_page():
    users = User.get_all()
    views = View.get_all()
    if request.method == "POST":
        search_term = request.form['search_term']
        user = User.search(search_term)
        if user:
            return redirect(
                url_for('user.update', id=user.id)
            )
        view = View.search(search_term)
        if view:
            return redirect(
                url_for('view.update', id=view.id)
            )

    return render_template(
        "admin/main-page.html",
        user_heads=username_head,
        users=users,
        views=views
    )
