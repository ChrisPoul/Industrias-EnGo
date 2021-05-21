from flask import session
from . import UserTest
from EnGo.models.user import User


class UserRequestTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)


class TestRegister(UserRequestTest):

    def test_should_register_user_given_valid_user(self):
        user = User(
            username="Valid UserName",
            password="0000"
        )
        user.request.register()

        self.assertIn(user, self.db.session)

    def test_should_not_register_user_given_invalid_user(self):
        user = User(
            username="",
            password=""
        )
        user.request.register()

        self.assertNotIn(user, self.db.session)


class TestLogin(UserRequestTest):

    def test_should_login_user_given_valid_credentials(self):
        user = User(
            username=self.user.username,
            password=self.user.password
        )
        user.request.login()

        self.assertEqual(session["user_id"], self.user.id)
        

    def test_should_not_login_user_given_invalid_credentials(self):
        user = User(
            username="Non existent username",
            password="0000"
        )
        user.request.login()

        with self.assertRaises(KeyError):
            session["user_id"]


class TestUpdate(UserRequestTest):

    def test_should_update_user_given_valid_changes(self):
        self.user.username = "Valid Username"
        self.user.request.update()
        self.db.session.rollback()

        self.assertEqual(self.user.username, "Valid Username")

    def test_should_not_update_user_given_invalid_changes(self):
        self.user.username = ""
        self.user.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.user.username, "")
