from . import UserTest
from flask import url_for
from datetime import datetime
from werkzeug.security import (
    generate_password_hash, check_password_hash
)
from EnGo.models.user import User
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class UserViewTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.user.password = generate_password_hash(self.user.password)
        self.user.update()
        self.create_test_users()


class TestUsersView(UserViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            response = client.get(
                url_for('user.users')
            )
        
        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('user.users')
            )

        self.assertStatus(response, 302)

    def test_should_redirect_given_valid_search_term_and_LUHP(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Test User"
        )
        with self.client as client:
            response = client.post(
                url_for('user.users'),
                data=search_data
            )
        
        self.assertStatus(response, 302)

    def test_should_not_redirect_given_invalid_search_term_and_LUHP(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Invalid term"
        )
        with self.client as client:
            response = client.post(
                url_for('user.users'),
                data=search_data
            )
        
        self.assert200(response)


class TestRegisterView(UserViewTest):

    def test_should_register_user_given_valid_credentials_and_LUHP(self):
        self.login_user(self.admin_user)
        user_credentials = dict(
            username="Some User",
            password="0000",
            password_confirm="0000",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.register'),
                data=user_credentials
            )
        
        self.assertNotEqual(User.search('Some User'), None)

    def test_should_not_register_user_given_invalid_username_and_LUHP(self):
        self.login_user(self.admin_user)
        user_credentials = dict(
            username="Test",
            password="",
            password_confirm="",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.register'),
                data=user_credentials
            )

        self.assertEqual(User.search('Test'), None)

    def test_should_not_register_user_given_passwords_dont_match_and_LUHP(self):
        self.login_user(self.admin_user)
        user_credentials = dict(
            username="Test",
            password="0000",
            password_confirm="1234",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.register'),
                data=user_credentials
            )

        self.assertEqual(User.search('Test'), None)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        response = self.client.get(
                url_for('user.register')
            )

        self.assertStatus(response, 302)


class TestLoginView(UserViewTest):

    def test_should_login_user_given_valid_credentials_and_no_LU(self):
        user_credentials = dict(
            username="Test User",
            password="0000"
        )
        with self.client as client:
            client.post(
                url_for('user.login'),
                data=user_credentials
            )
        with self.client.session_transaction() as session:
            self.assertEqual(session['user_id'], self.user.id)
        
    def test_should_not_login_user_given_invalid_credentials_and_no_LU(self):
        user_credentials = dict(
            username="Invalid username",
            password="invalid password"
        )
        with self.client as client:
            client.post(
                url_for('user.login'),
                data=user_credentials
            )
        with self.client.session_transaction() as session:
            with self.assertRaises(KeyError):
                session['user_id']

    def test_should_redirect_given_LU(self):
        self.login_user(self.admin_user)
        response = self.client.get(
            url_for('user.login')
        )
        
        self.assertStatus(response, 302)


class TestLogoutView(UserViewTest):

    def test_should_logout_user_given_LU(self):
        self.login_user(self.normal_user)
        with self.client as client:
            client.get(
                url_for('user.logout')
            )
        
        with self.client.session_transaction() as session:
            with self.assertRaises(KeyError):
                session['user_id']

    def test_should_redirect_given_LU(self):
        self.login_user(self.admin_user)
        response = self.client.get(
            url_for('user.logout')
        )
        
        self.assertStatus(response, 302)

    def test_should_redirect_given_no_LU(self):
        response = self.client.get(
            url_for('user.logout')
        )
        
        self.assertStatus(response, 302)
    

class TestUpdateView(UserViewTest):

    def test_should_update_user_given_valid_user_data_and_LUHP(self):
        self.login_user(self.admin_user)
        user_data = dict(
            username="New Username",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.update', id=self.user.id),
                data=user_data
            )
        self.db.session.rollback()

        self.assertEqual(self.user.username, "New Username")

    def test_should_not_update_user_given_invalid_user_data_and_LUHP(self):
        self.login_user(self.admin_user)
        user_data = dict(
            username="",
            password="0000",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.update', id=self.user.id),
                data=user_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.user.username, "")

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('user.update', id=self.user.id)
            )

        self.assertStatus(response, 302)


class TestUpdatePassword(UserViewTest):

    def test_should_update_user_password_given_valid_password_and_LUHP(self):
        self.login_user(self.admin_user)
        password_data = dict(
            password="new password",
            password_confirm="new password"
        )
        with self.client as client:
            client.post(
                url_for('user.update_password', id=self.user.id),
                data=password_data
            )
        
        self.assertTrue(check_password_hash(self.user.password, "new password"))

    def test_should_not_update_password_given_invalid_password_and_LUHP(self):
        self.login_user(self.admin_user)
        password_data = dict(
            password="some password",
            password_confirm="new password"
        )
        with self.client as client:
            client.post(
                url_for('user.update_password', id=self.user.id),
                data=password_data
            )

        self.assertFalse(check_password_hash(self.user.password, ""))


class TestDeleteView(UserViewTest):

    def test_should_delete_user_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            client.get(
                url_for('user.delete', id=self.normal_user.id)
            )

        self.assertNotIn(self.normal_user, self.db.session)


class TestProfileView(UserViewTest):

    def test_should_grant_access_given_LUHP(self):
        self.login_user(self.dev_user)
        with self.client as client:
           response = client.get(
                url_for('user.profile', id=self.normal_user.id)
            )

        self.assert200(response)

    def test_should_grant_access_given_profile_belongs_to_LU(self):
        self.login_user(self.normal_user)
        with self.client as client:
           response = client.get(
                url_for('user.profile', id=self.normal_user.id)
            )

        self.assert200(response)


class TestAssignActivityView(UserViewTest):

    def test_should_add_activity_given_valid_activity_input_and_LUHP(self):
        self.login_user(self.dev_user)
        activity_input = dict(
            title="Test Activity",
            description="",
            due_date="2020-06-30"
        )
        with self.client as client:
            client.post(
                url_for('user.assign_activity', id=self.user.id),
                data=activity_input
            )
        
        self.assertEqual(len(self.user.activities), 1)

    def test_should_not_add_activity_given_invalid_title_and_LUHP(self):
        self.login_user(self.dev_user)
        activity_input = dict(
            title="",
            description="",
            due_date="2020-06-30"
        )
        with self.client as client:
            client.post(
                url_for('user.assign_activity', id=self.user.id),
                data=activity_input
            )
        
        self.assertEqual(len(self.user.activities), 0)

    def test_should_not_add_activity_given_invalid_due_date_and_LUHP(self):
        self.login_user(self.dev_user)
        activity_input = dict(
            title="Test Title",
            description="",
            due_date=""
        )
        with self.client as client:
            client.post(
                url_for('user.assign_activity', id=self.user.id),
                data=activity_input
            )
        
        self.assertEqual(len(self.user.activities), 0)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('user.assign_activity', id=self.user.id)
            )

        self.assertStatus(response, 302)
    

class TestDayActivities(UserViewTest):

    def test_should_grant_access_given_LUHP(self):
        self.login_user(self.dev_user)
        with self.client as client:
            response = client.get(
                url_for('user.day_activities', 
                id=self.normal_user.id,
                date_str=datetime.today().strftime("%Y-%m-%d")
                )
            )
        
        self.assert200(response)
        