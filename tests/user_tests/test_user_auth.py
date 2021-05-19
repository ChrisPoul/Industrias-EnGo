from flask import url_for, session, g
from . import UserTest
from EnGo.models.user import User
from EnGo.models.user.auth import UserAuth


class UserAuthTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.auth = UserAuth()


class TestLoginUser(UserAuthTest):

    def test_should_login_user_given_valid_credentials(self):
        user_credentials = dict(
            username="Test User",
            password="0000"
        )
        url = url_for('auth.login')
        with self.request_context(url, user_credentials):
            self.auth.login_user()
            loged_in_user_id = session["user_id"]
            
        self.assertEqual(loged_in_user_id, self.user.id)

    def test_should_not_login_user_given_invalid_credentials(self):
        user_credentials = dict(
            username="Invalid username",
            password="invalid password"
        )
        url = url_for('auth.login')
        with self.request_context(url, user_credentials):
            self.auth.login_user()
            with self.assertRaises(KeyError):
                session["user_id"]

    def test_should_return_none_given_valid_credentials(self):
        user_credentials = dict(
            username="Test User",
            password="0000"
        )
        url = url_for('auth.login')
        with self.request_context(url, user_credentials):
            error = self.auth.login_user()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_credentials(self):
        user_credentials = dict(
            username="Invalid username",
            password="invalid password"
        )
        url = url_for('auth.login')
        with self.request_context(url, user_credentials):
            error = self.auth.login_user()

        self.assertNotEqual(error, None)
            

class TestRegisterUser(UserAuthTest):

    def test_should_register_user_given_valid_credentials(self):
        user_credentials = dict(
            username="Test2",
            password="0000"
        )
        url = url_for('auth.register')
        with self.request_context(url, user_credentials):
            self.auth.register_user()

        self.assertEqual(len(User.get_all()), 2)

    def test_should_not_register_user_given_invalid_credentials(self):
        user_credentials = dict(
            username="Test",
            password=""
        )
        url = url_for('auth.register')
        with self.request_context(url, user_credentials):
            self.auth.register_user()

        self.assertEqual(len(User.get_all()), 1)

    def test_should_return_none_given_valid_credentials(self):
        user_credentials = dict(
            username="Test2",
            password="0000"
        )
        url = url_for('auth.register')
        with self.request_context(url, user_credentials):
            error = self.auth.register_user()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_credentials(self):
        user_credentials = dict(
            username="Test",
            password=""
        )
        url = url_for('auth.register')
        with self.request_context(url, user_credentials):
            error = self.auth.register_user()

        self.assertNotEqual(error, None)


class TestLogoutUser(UserAuthTest):

    def test_should_logout_user(self):
        self.login_user(self.user)
        self.auth.logout_user()

        with self.assertRaises(KeyError):
            session["user_id"]


class TestDeleteUser(UserAuthTest):

    def test_should_delete_user_given_valid_user_id(self):
        self.auth.delete_user(self.user.id)

        self.assertNotIn(self.user, self.db.session)


class TestLoadLogedInUser(UserAuthTest):

    def test_should_add_user_to_g_given_valid_user_id_in_session(self):
        session["user_id"] = self.user.id
        self.auth.load_loged_in_user()

        self.assertEqual(g.user, self.user)

    def test_should_set_user_as_null_given_invalid_user_id(self):
        session["user_id"] = 100
        self.auth.load_loged_in_user()

        self.assertEqual(g.user, None)