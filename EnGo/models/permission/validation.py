from . import permission_attributes
from EnGo.models import has_nums
from EnGo.errors.messages import (
    empty_value_error, repeated_value_error
)


class PermissionValidation:

    def __init__(self, permission):
        self.permission = permission
        self.error = None

    def validate(self):
        self.validate_empty_values()
        self.validate_name()
        self.validate_unique_values()

        return self.error

    def validate_empty_values(self):
        for attribute in permission_attributes:
            self.validate_empty_value(attribute)
            
        return self.error

    def validate_empty_value(self, attribute):
        value = getattr(self.permission, attribute)
        if value == "":
            self.error = empty_value_error
        
        return self.error

    def validate_name(self):
        if has_nums(self.permission.permission_name):
            self.error = "El nombre no puede llevar números"
        
        return self.error

    def validate_unique_values(self):
        from . import Permission
        permission = Permission.search(self.permission.permission_name)
        if permission and permission is not self.permission:
            self.error = repeated_value_error

        return self.error
    