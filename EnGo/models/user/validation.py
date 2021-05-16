from . import user_attributes


class UserValidation:

    def __init__(self, user):
        self.user = user
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_unique_values()
        
        return self.error

    def validate_empty_values(self):
        for attribute in user_attributes:
            self.error = self.validate_empty_value(attribute)
            if self.error:
                return self.error

    def validate_empty_value(self, attribute):
        value = getattr(self.user, attribute)
        if value == "":
            return "No se pueden dejar campos en blanco"

    def validate_unique_values(self):
        from . import User
        user = User.search(self.user.username)
        if user:
            self.error = "Nombre de usuario no disponible"
        
        return self.error
