from .setup import Test
from EnGo.models import commit_to_db, create_admin_user
from EnGo.models.user import User


class TestCommitToDb(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test",
            password="0000"
        )
        self.user.add()

    def test_should_save_changes_made_to_user(self):
        self.user.username = "New Name"
        commit_to_db()
        self.db.session.rollback()

        self.assertEqual(self.user.username, "New Name")


class TestCreateAdminUser(Test):

    def test_should_create_user_with_admin_permission_given_username(self):
        create_admin_user("Admin")
        user = User.get(1)

        self.assertEqual(user.username, "Admin")
        self.assertEqual(len(user.permissions), 1)

