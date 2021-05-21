from flask import session
from . import User


class UserRequest:

    def __init__(self, user):
        self.user = user

    def login(self):
        user = User.search(self.user.username)
        error = None
        if not user:
            error = "Nombre de usuario incorrecto"
        elif self.user.password != user.password:
            error = "Contraseña incorrecta"
        if not error:
            session.clear()
            session['user_id'] = user.id

        return error

    def register(self):
        error = self.user.validation.validate()
        if not error:
            self.user.add()

        return error
