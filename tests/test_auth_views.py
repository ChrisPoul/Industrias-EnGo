from . import Test
from flask import url_for
from EnGo.models.user import User, UserPermission
from EnGo.models.permission import Permission


class AuthViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.admin_user = User(
            username="Admin User",
            password="0000"
        )
        self.admin_user.add()
        self.permission = Permission(
            permission_name="admin",
        )
        self.permission.add()
        user_permission = UserPermission(
            user_id=self.admin_user.id,
            permission_id=self.permission.id
        )
        user_permission.add()
        self.normal_user = User(
            username="Normal User",
            password="0000"
        )
        self.normal_user.add()


class TestRegisterView(AuthViewTest):

    def test_should_grant_access_given_logged_in_user_is_admin(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.admin_user.id
        response = self.client.get(
            url_for('auth.register')
        )

        self.assert200(response)

    def test_should_return_redirect_given_logged_in_user_is_not_admin(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
                url_for('auth.register')
            )

        self.assertStatus(response, 302)


class TestLoginView(AuthViewTest):

    def test_should_grant_access_given_no_loged_in_user(self):
        response = self.client.get(
            url_for('auth.login')
        )

        self.assert200(response)

    def test_should_return_redirect_given_logged_in_user(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for('auth.login')
        )
        
        self.assertStatus(response, 302)


class TestLogoutView(AuthViewTest):

    def test_should_redirect_given_loged_in_user(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for('auth.logout')
        )
        
        self.assertStatus(response, 302)

    def test_should_redirect_given_no_loged_in_user(self):
        response = self.client.get(
            url_for('auth.logout')
        )
        
        self.assertStatus(response, 302)
