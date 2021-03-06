from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values


class UserValidation:

    def __init__(self, user):
        self.user = user
        self.error = None

    def validate(self):
        self.validate_empty_values()
        self.validate_unique_values()
        
        return self.error

    def validate_empty_values(self):
        user_attributes = [
            "username",
            "password",
            "salary"
        ]
        self.error = validate_empty_values(self.user, user_attributes)
        
        return self.error

    def validate_unique_values(self):
        from . import User
        user = User.search(self.user.username)
        if user and user is not self.user:
            self.error = repeated_value_error
        
        return self.error
