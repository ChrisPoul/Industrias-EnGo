from flask import session
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from . import User


class UserRequest:

    def __init__(self, user):
        self.user = user

    def login(self):
        user = User.search(self.user.username)
        error = None
        if not user:
            error = "Nombre de usuario incorrecto"
        elif not check_password_hash(user.password, self.user.password):
            error = "Contraseña incorrecta"
        if not error:
            session.clear()
            session['user_id'] = user.id

        return error

    def register(self):
        error = self.user.validation.validate()
        if not error:
            self.user.password = generate_password_hash(self.user.password)
            self.user.add()

        return error

    def update(self):
        error = self.user.validation.validate()
        if not error:
            self.user.update()

        return error


class UserActivityRequest:

    def __init__(self, user_activity):
        self.activity = user_activity
    
    def add(self):
        error = self.activity.validation.validate()
        if not error:
            self.activity.add()
        
        return error

    def update(self):
        error = self.activity.validation.validate()
        if not error:
            self.activity.update()
        
        return error


class UserProductionRequest:

    def __init__(self, user_production):
        self.user_production = user_production

    def add(self):
        error = self.user_production.validation.validate()
        if not error:
            self.user_production.add()
    
    def update(self):
        error = self.user_production.validation.validate()
        if not error:
            self.user_production.update()
        
        return error
