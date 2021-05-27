from . import UserTest
from flask import url_for
from werkzeug.security import generate_password_hash
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
            password="New password"
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
            password="0000"
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


class TestDeleteView(UserViewTest):

    def test_should_delete_user_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            client.get(
                url_for('user.delete', id=self.normal_user.id)
            )

        self.assertNotIn(self.normal_user, self.db.session)
