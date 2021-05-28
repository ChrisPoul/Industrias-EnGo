from . import PermissionTest
from EnGo.models.permission import Permission

    
class TestValidate(PermissionTest):

    def test_should_not_return_error_given_valid_permission(self):
        permission = Permission(
            permission_name="production",
        )
        error = permission.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_permission(self):
        permission = Permission(
            permission_name="",
        )
        error = permission.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(PermissionTest):

    def test_should_not_return_error_given_non_empty_values(self):
        permission = Permission(
            permission_name="production",
        )
        error = permission.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_values(self):
        permission = Permission(
            permission_name="",
        )
        error = permission.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateName(PermissionTest):

    def test_should_not_return_error_given_valid_name(self):
        permission = Permission(
            permission_name="production",
        )
        error = permission.validation.validate_name()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_name(self):
        permission = Permission(
            permission_name="production2",
        )
        error = permission.validation.validate_name()

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(PermissionTest):

    def test_should_not_return_error_given_unique_values(self):
        permission = Permission(
            permission_name="production",
        )
        error = permission.validation.validate_unique_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_values(self):
        permission = Permission(
            permission_name="admin",
        )
        error = permission.validation.validate_unique_values()

        self.assertNotEqual(error, None)

    def test_should_not_return_error_when_validating_registered_permission(self):
        error = self.admin_permission.validation.validate_unique_values()

        self.assertEqual(error, None)
