from . import permission_attributes
from EnGo.models import has_nums
from EnGo.errors.messages import repeated_value_error
from EnGo.models import validate_empty_values


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
        self.error = validate_empty_values(self.permission, permission_attributes)
            
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
    