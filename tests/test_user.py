from . import Test
from EnGo.models.user import User


class UserTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test",
            password="0000"
        )
        self.user.add()


class TestAdd(Test):

    def test_should_add_user(self):
        user = User(
            username="Test",
            password="0000"
        )
        user.add()

        self.assertIn(user, self.db.session)


class TestUpdate(UserTest):

    def test_should_update_user(self):
        self.user.username = "New username"
        self.user.update()
        self.db.session.rollback()

        self.assertEqual(self.user.username, "New username")


class TestDelete(UserTest):

    def test_should_delete_user(self):
        self.user.delete()

        self.assertNotIn(self.user, self.db.session)


class TestGet(UserTest):

    def test_should_return_user_given_valid_id(self):
        user = User.get(1)

        self.assertEqual(user, self.user)

    def test_should_return_none_given_invalid_id(self):
        user = User.get(2)

        self.assertEqual(user, None)


class TestGetAll(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.user2 = User(
            username="Test2",
            password="0000"
        )
        self.user2.add()

    def test_should_return_list_of_all_users(self):
        users = User.get_all()

        self.assertEqual(users, [self.user, self.user2])


class TestSearch(UserTest):

    def test_should_return_permission_given_valid_username(self):
        user = User.search("Test")

        self.assertEqual(user, self.user)

    def test_should_return_none_given_invalid_username(self):
        user = User.search("Non existent name")

        self.assertEqual(user, None)
