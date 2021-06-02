from tests import Test
from EnGo.models import (
    commit_to_db, has_nums
)
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


class TestHasNums(Test):

    def test_should_return_false_given_string_with_no_numbers(self):
        self.assertFalse(has_nums("string with no numbers"))

    def test_should_return_true_given_string_with_numbers(self):
        self.assertTrue(has_nums("s0m3 number5"))

