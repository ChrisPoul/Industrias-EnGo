from . import user_attributes
from EnGo.errors.messages import (
    repeated_value_error, empty_value_error
)


class UserValidation:

    def __init__(self, user):
        self.user = user
        self.error = None

    def validate(self):
        self.validate_empty_values()
        self.validate_unique_values()
        
        return self.error

    def validate_empty_values(self):
        for attribute in user_attributes:
            self.validate_empty_value(attribute)
            
        return self.error

    def validate_empty_value(self, attribute):
        value = getattr(self.user, attribute)
        if value == "":
            self.error = empty_value_error
        
        return self.error

    def validate_unique_values(self):
        from . import User
        user = User.search(self.user.username)
        if user and user is not self.user:
            self.error = repeated_value_error
        
        return self.error
