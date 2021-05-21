from flask import url_for, session, g
from . import UserTest
from EnGo.models.user import User
from EnGo.models.user.auth import UserAuth


class UserAuthTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.auth = UserAuth()


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
