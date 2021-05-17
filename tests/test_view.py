from . import Test
from EnGo.models.view import View


class UserTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.view = View(
            view_name="Test"
        )
        self.view.add()


class TestAdd(Test):

    def test_should_add_view(self):
        view = View(
            view_name="Test"
        )
        view.add()

        self.assertIn(view, self.db.session)


class TestUpdate(UserTest):

    def test_should_update_view(self):
        self.view.view_name = "New name"
        self.view.update()
        self.db.session.rollback()

        self.assertEqual(self.view.view_name, "New name")


class TestDelete(UserTest):

    def test_should_delete_view(self):
        self.view.delete()

        self.assertNotIn(self.view, self.db.session)


class TestGet(UserTest):

    def test_should_return_view_given_valid_id(self):
        view = View.get(1)

        self.assertEqual(view, self.view)

    def test_should_return_none_given_invalid_id(self):
        view = View.get(2)

        self.assertEqual(view, None)


class TestGetAll(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.view2 = View(
            view_name="Test2"
        )
        self.view2.add()

    def test_should_return_list_of_all_views(self):
        views = View.get_all()

        self.assertEqual(views, [self.view, self.view2])


class TestSearch(UserTest):

    def test_should_return_permission_given_valid_name(self):
        view = View.search("Test")

        self.assertEqual(view, self.view)

    def test_should_return_none_given_invalid_name(self):
        view = View.search("Non existent name")

        self.assertEqual(view, None)