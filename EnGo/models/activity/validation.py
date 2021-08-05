from EnGo.models import validate_empty_values


class UserActivityValidation:

    def __init__(self, user_activity):
        self.activity = user_activity
        self.error = None

    def validate(self):
        self.validate_empty_values()

        return self.error

    def validate_empty_values(self):
        self.error = validate_empty_values(self.activity, ["title"])

        return self.error