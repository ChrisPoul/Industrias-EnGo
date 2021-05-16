from . import permission_attributes


class PermissionValidation:

    def __init__(self, permission):
        self.permission = permission
        self.error = None

    def validate(self):
        self.validate_empty_values()
        if not self.error:
            self.validate_name()
        if not self.error:
            self.validate_unique_values()

        return self.error

    def validate_empty_values(self):
        for attribute in permission_attributes:
            self.error = self.validate_empty_value(attribute)
            if self.error:
                return self.error

    def validate_empty_value(self, attribute):
        value = getattr(self.permission, attribute)
        if value == "":
            return "No se pueden dejar campos vacíos"

    def validate_name(self):
        pass

    def validate_unique_values(self):
        from . import Permission
        permission = Permission.search(self.permission.permission_name)
        if permission and permission is not self.permission:
            self.error = "Ese nombre no está disponible"

        return self.error
    