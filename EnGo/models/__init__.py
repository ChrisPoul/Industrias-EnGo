from flask_sqlalchemy import SQLAlchemy
from EnGo.errors.messages import (
    empty_value_error, invalid_num_error
)

db = SQLAlchemy(session_options={"autoflush": False})


class MyModel:

    def add(self):
        db.session.add(self)
        commit_to_db()
    
    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        commit_to_db()

    @property
    def request(self):
        from .request import ObjectRequest
        return ObjectRequest(self)


def commit_to_db():
    db.session.commit()


def has_nums(some_string):
    nums = "1234567890"
    for char in some_string:
        if char in nums:
            return True

    return False


def validate_empty_values(obj, attributes):
    for attribute in attributes:
        value = getattr(obj, attribute)
        if value == "":
            return empty_value_error
        
    return None


def validate_obj_num_attrs(obj, attributes):
    for attr in attributes:
        error = validate_obj_num(obj, attr)
        if error:
            break

    return error
            

def validate_obj_num(obj, attribute):
    num = getattr(obj, attribute)
    error = None
    if not num:
        num = 0
    try:
        num = float(num)
    except ValueError:
        num = 0
        error = invalid_num_error
    setattr(obj, attribute, num)
    if not error:
        if num < 0:
            error = "No se pueden añadir cantidades negativas"

    return error