from . import UserTest
from EnGo.models.user import User


class TestValidate(UserTest):

    def test_should_not_return_error_given_valid_user(self):
        user = User(
            username="Test 2",
            password="0000"
        )
        error = user.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_user(self):
        user = User(
            username="Test",
            password=""
        )
        error = user.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(UserTest):

    def test_should_not_return_error_given_non_empty_values(self):
        user = User(
            username="Test",
            password="0000"
        )
        error = user.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_values(self):
        user = User(
            username="",
            password=""
        )
        error = user.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateEmptyValue(UserTest):

    def test_should_not_return_error_given_non_empty_username(self):
        user = User(
            username="Test",
            password=""
        )
        error = user.validation.validate_empty_value("username")

        self.assertEqual(error, None)

    def test_should_not_return_error_given_non_empty_password(self):
        user = User(
            username="",
            password="0000"
        )
        error = user.validation.validate_empty_value("password")

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_username(self):
        user = User(
            username="",
            password="0000"
        )
        error = user.validation.validate_empty_value("username")

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_password(self):
        user = User(
            username="Test",
            password=""
        )
        error = user.validation.validate_empty_value("password")

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(UserTest):

    def test_should_not_return_error_given_unique_username(self):
        user = User(
            username="Unique name",
            password="0000"
        )
        error = user.validation.validate_unique_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_username(self):
        user = User(
            username="Test User",
            password="0000"
        )
        error = user.validation.validate_unique_values()

        self.assertNotEqual(error, None)

    def test_should_not_return_error_when_validating_registered_user(self):
        error = self.user.validation.validate_unique_values()

        self.assertEqual(error, None)
