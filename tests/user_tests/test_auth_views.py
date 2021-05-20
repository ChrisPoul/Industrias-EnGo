from . import UserTest
from flask import url_for
from EnGo.models.user import User
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###


class AuthViewTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.create_test_users()


class TestRegisterView(AuthViewTest):

    def test_should_grant_access_given_LU_is_admin(self):
        self.login_user(self.admin_user)
        response = self.client.get(
            url_for('auth.register')
        )

        self.assert200(response)

    def test_should_return_redirect_given_LU_is_not_admin(self):
        self.login_user(self.normal_user)
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
                url_for('auth.register')
            )

        self.assertStatus(response, 302)


class TestLoginView(AuthViewTest):

    def test_should_return_valid_response_given_no_LU(self):
        response = self.client.get(
            url_for('auth.login')
        )

        self.assert200(response)

    def test_should_redirect_given_LU(self):
        self.login_user(self.admin_user)
        response = self.client.get(
            url_for('auth.login')
        )
        
        self.assertStatus(response, 302)


class TestLogoutView(AuthViewTest):

    def test_should_redirect_given_LU(self):
        self.login_user(self.admin_user)
        response = self.client.get(
            url_for('auth.logout')
        )
        
        self.assertStatus(response, 302)

    def test_should_redirect_given_no_LU(self):
        response = self.client.get(
            url_for('auth.logout')
        )
        
        self.assertStatus(response, 302)
