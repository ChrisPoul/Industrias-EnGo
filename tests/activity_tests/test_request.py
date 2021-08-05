from datetime import date
from . import ActivityTest
from EnGo.models.activity import Activity


class TestRequestAdd(ActivityTest):

    def test_should_add_activity_given_valid_activity(self):
        activity = Activity(
            user_id=self.user.id,
            title="Test Activity",
            description=""
        )
        activity.request.add()

        self.assertIn(activity, self.db.session)

    def test_should_not_add_activity_given_invalid_activity(self):
        activity = Activity(
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