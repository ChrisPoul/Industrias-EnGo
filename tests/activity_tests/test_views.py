from . import ActivityTest
from datetime import datetime
from flask import url_for
from EnGo.models.activity import Activity

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ActivityViewTest(ActivityTest):

    def setUp(self):
        ActivityTest.setUp(self)
        self.activity.delete()
        self.create_test_users()


class TestAssignView(ActivityViewTest):

    def test_should_add_activity_given_valid_activity_input_and_LUHP(self):
        self.login_user(self.dev_user)
        activity_input = dict(
            title="Test Activity",
            description="",
            user_id=self.user.id
        )
        with self.client as client:
            client.post(
                url_for('activity.assign'),
                data=activity_input
            )
        
        self.assertEqual(len(self.user.activities), 1)

    def test_should_not_add_activity_given_invalid_title_and_LUHP(self):
        self.login_user(self.dev_user)
        activity_input = dict(
            title="",
            description="",
            user_id=self.user.id
        )
        with self.client as client:
            client.post(
                url_for('activity.assign'),
                data=activity_input
            )
        
        self.assertEqual(len(self.user.activities), 0)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('activity.assign')
            )

        self.assertStatus(response, 302)


class TestUpdateView(ActivityViewTest):

    def setUp(self):
        ActivityViewTest.setUp(self)
        self.activity = Activity(
            user_id=self.user.id,
            title="New Activity"
        )
        self.activity.add()

    def test_should_update_activity_given_valid_activity_input_and_LUHP(self):
        self.login_user(self.admin_user)
        activity_input = dict(
            title="New Activity",
            description="Test Description",
            user_id=self.user.id
        )
        with self.client as client:
            client.post(
                url_for('activity.update', activity_id=self.activity.id),
                data=activity_input
            )
        self.db.session.rollback()
        
        self.assertEqual(self.activity.title, "New Activity")

    def test_should_not_update_activity_given_invalid_activity_input_and_LUHP(self):
        self.login_user(self.admin_user)
        activity_input = dict(
            title="",
            description="Test Description",
            user_id=self.user.id
        )
        with self.client as client:
            client.post(
                url_for('activity.update', activity_id=self.activity.id),
                data=activity_input
            )
        self.db.session.rollback()
        
        self.assertNotEqual(self.activity.title, "")

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('activity.update', activity_id=self.activity.id)
            )
        
        self.assertStatus(response, 302)
