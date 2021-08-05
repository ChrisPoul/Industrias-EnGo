from datetime import date
from . import ActivityTest
from EnGo.models.activity import Activity


class TestValidate(ActivityTest):

    def test_should_not_return_error_given_valid_activity(self):
        activity = Activity(
            user_id=self.user.id,
            title="Test Activity",
            description=""
        )
        error = activity.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_activity(self):
        activity = Activity(
            user_id=self.user.id,
            title="",
            description="Test Description"
        )
        error = activity.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(ActivityTest):

    def test_should_not_return_error_given_no_empty_title(self):
        activity = Activity(
            user_id=self.user.id,
            title="Test Activity",
            description=""
        )
        error = activity.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_title(self):
        activity = Activity(
            user_id=self.user.id,
            title="",
            description="Test Description"
        )
        error = activity.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateUserId(ActivityTest):

    def test_should_not_return_error_given_valid_user_id(self):
        activity = Activity(
            user_id=self.user.id
        )
        error = activity.validation.validate_user_id()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_user_id(self):
        activity = Activity(
            user_id=0
        )
        error = activity.validation.validate_user_id()

        self.assertNotEqual(error, None)
