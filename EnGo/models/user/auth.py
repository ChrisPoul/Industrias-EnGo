from flask import (
    session, request, g
)
from . import User


class UserAuth:

    def login_user(self):
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

    def register_user(self):
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

    def logout_user(self):
        session.clear()

    def delete_user(self, user_id):
        user = User.get(user_id)
        user.delete()

    def load_loged_in_user(self):
        try:
            user_id = session["user_id"]
        except KeyError:
            user_id = None

        if user_id is None:
            g.user = None
        else:
            g.user = User.get(user_id)
