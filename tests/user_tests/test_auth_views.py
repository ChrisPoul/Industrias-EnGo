from . import UserTest
from flask import url_for
from EnGo.models.user import User
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class AuthViewTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.create_test_users()


class TestRegisterView(AuthViewTest):

    def test_should_register_user_given_valid_credentials_and_LUHP(self):
        self.login_user(self.admin_user)
        user_credentials = dict(
            username="Some User",
            password="0000"
        )
        with self.client as client:
            client.post(
                url_for('user.register'),
                data=user_credentials
            )
        
        self.assertNotEqual(User.search('Some User'), None)

    def test_should_not_register_user_given_invalid_credentials_and_LUHP(self):
        self.login_user(self.admin_user)
        user_credentials = dict(
            username="Test",
            password=""
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


class TestLoginView(AuthViewTest):

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


class TestLogoutView(AuthViewTest):

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
    

class TestUpdateView(AuthViewTest):

    def test_should_update_user_given_valid_user_data(self):
        pass


class TestDeleteView(AuthViewTest):

    def test_should_delete_user_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            client.get(
                url_for('user.delete', id=self.normal_user.id)
            )

        self.assertNotIn(self.normal_user, self.db.session)
