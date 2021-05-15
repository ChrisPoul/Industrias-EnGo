from flask import (
    redirect, url_for, session,
    request, g
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

        return error

    def register(self):
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.search(username)
        if user:
            error = "Nombre de usuario no disponible"
        if password == "":
            error = "Contraseña invalida"

        if not error:
            user = User(
                username=username,
                password=password
            )
            user.add()

        return error

    def logout(self):
        session.clear()

    def load_loged_in_user(self):
        try:
            user_id = session["user_id"]
        except KeyError:
            user_id = None

        if user_id is None:
            g.user = None
        else:
            g.user = User.get(user_id)


def login_required(view):
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(
                url_for('auth.login')
            )
        return view(**kwargs)

    return wrapped_view
