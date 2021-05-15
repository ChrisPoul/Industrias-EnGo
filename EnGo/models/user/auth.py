from flask import (
    redirect, url_for, current_app,
    session, request, g
)
from . import User


class Auth:

    def login(self):
        username = request.form["username"]
        password = request.form["password"]
        error = None

        user = User.search(username)
        if not user:
            error = "Nombre de usuario incorrecto"
        elif password != user.password:
            error = "Contraseña incorrecta"

        if not error:
            session.clear()
            session['user_id'] = user.id

    def logout(self):
        session.clear()


def login_required(view):
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(
                url_for('auth.login')
            )
        return view(**kwargs)
    
    return wrapped_view


@current_app.before_request
def load_loged_in_user():
    try:
        user_id = session["user_id"]
    except KeyError:
        user_id = None

    if user_id is None:
        g.user = None
    else:
        g.user = User.get(user_id)
