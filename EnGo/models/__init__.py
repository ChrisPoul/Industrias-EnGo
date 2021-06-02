from flask_sqlalchemy import SQLAlchemy
from EnGo.errors.messages import empty_value_error

db = SQLAlchemy()


class MyModel:

    def add(self):
        db.session.add(self)
        commit_to_db()
    
    def update(self):
        commit_to_db()

    def delete(self):
        db.session.delete(self)
        commit_to_db()


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
