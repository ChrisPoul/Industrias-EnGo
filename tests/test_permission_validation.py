from .setup import Test
from EnGo.models.permission import Permission


class PermissionValidationTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.permission = Permission(
            permission_name="admin",
            description="Gives acces to all aspects of the system"
        )
        self.permission.add()

    
class TestValidate(PermissionValidationTest):

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


class TestValidateEmptyValues(PermissionValidationTest):

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


class TestValidateEmptyValue(PermissionValidationTest):

    def test_should_not_return_error_given_non_empty_name(self):
        permission = Permission(
            permission_name="production",
        )
        error = permission.validation.validate_empty_value("permission_name")

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_name(self):
        permission = Permission(
            permission_name="",
        )
        error = permission.validation.validate_empty_value("permission_name")

        self.assertNotEqual(error, None)


class TestValidateName(PermissionValidationTest):

    def test_should_not_return_error_given_valid_name(self):
        permission = Permission(
            permission_name="production",
        )
        error = permission.validation.validate_name()

        self.assertEqual(error, None)


class TestValidateUniqueValues(PermissionValidationTest):

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
        error = self.permission.validation.validate_unique_values()

        self.assertEqual(error, None)
