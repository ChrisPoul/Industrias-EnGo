from flask import (
    Blueprint, render_template, request,
    redirect, url_for
)
from . import permission_required, login_required
from .user import users_heads
from EnGo.models.user import User
from EnGo.models.view import View

bp = Blueprint('admin', __name__, url_prefix="/admin")

@bp.route("/main_page", methods=('POST', 'GET'))
@permission_required(["admin"])
@login_required
def main_page():
    users = User.get_all()
    views = View.get_all()
    if request.method == "POST":
        user = User.search(request.form['username'])
        if user:
            return redirect(
                url_for('user.update', id=user.id)
            )

    return render_template(
        "admin/main-page.html",
        user_heads=users_heads,
        users=users,
        views=views
    )
