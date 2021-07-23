from datetime import date
from . import UserTest
from EnGo.models.user import UserActivity


class ActivityTest(UserTest):
    
    def setUp(self):
        UserTest.setUp(self)
        self.activity = UserActivity(
            user_id=self.user.id,
            title="Test Activity",
            description="Test Description"
        )
        self.activity.add()


class TestValidate(ActivityTest):

    def test_should_not_return_error_given_valid_activity(self):
        activity = UserActivity(
            user_id=self.user.id,
            title="Test Activity",
            description=""
        )
        error = activity.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_activity(self):
        activity = UserActivity(
            user_id=self.user.id,
            title="",
            description="Test Description"
        )
        error = activity.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(ActivityTest):

    def test_should_not_return_error_given_no_empty_title(self):
        activity = UserActivity(
            user_id=self.user.id,
            title="Test Activity",
            description=""
        )
        error = activity.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_title(self):
        activity = UserActivity(
            user_id=self.user.id,
            title="",
            description="Test Description"
        )
        error = activity.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestRequestAdd(ActivityTest):

    def test_should_add_activity_given_valid_activity(self):
        activity = UserActivity(
            user_id=self.user.id,
            title="Test Activity",
            description=""
        )
        activity.request.add()

        self.assertIn(activity, self.db.session)

    def test_should_not_add_activity_given_invalid_activity(self):
        activity = UserActivity(
            user_id=self.user.id,
            title="",
            description=""
        )
        activity.request.add()

        self.assertNotIn(activity, self.db.session)


class TestRequestUpdate(ActivityTest):

    def test_should_update_activity_given_valid_changes(self):
        self.activity.title = "New Valid Title"
        self.activity.request.update()
        self.db.session.rollback()

        self.assertEqual(self.activity.title, "New Valid Title")

    def test_should_not_update_activity_given_invalid_changes(self):
        self.activity.title = ""
        self.activity.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.activity.title, "")
