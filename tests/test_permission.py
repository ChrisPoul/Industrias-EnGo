from . import Test
from EnGo.models.permission import Permission


class PermissionTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.permission = Permission(
            permission_name="Test"
        )
        self.permission.add()


class TestAdd(Test):

    def test_should_add_permission(self):
        permission = Permission(
            permission_name="Test"
        )
        permission.add()

        self.assertIn(permission, self.db.session)


class TestUpdate(PermissionTest):

    def test_should_update_permission(self):
        self.permission.permission_name = "New permission_name"
        self.permission.update()
        self.db.session.rollback()

        self.assertEqual(self.permission.permission_name, "New permission_name")


class TestDelete(PermissionTest):

    def test_should_delete_permission(self):
        self.permission.delete()

        self.assertNotIn(self.permission, self.db.session)


class TestGet(PermissionTest):

    def test_should_return_permission_given_valid_id(self):
        permission = Permission.get(1)

        self.assertEqual(permission, self.permission)

    def test_should_return_none_given_invalid_id(self):
        permission = Permission.get(2)

        self.assertEqual(permission, None)


class TestGetAll(PermissionTest):

    def setUp(self):
        PermissionTest.setUp(self)
        self.permission2 = Permission(
            permission_name="Test2"
        )
        self.permission2.add()

    def test_should_return_list_of_all_users(self):
        permissions = Permission.get_all()

        self.assertEqual(permissions, [self.permission, self.permission2])


class TestSearch(PermissionTest):

    def test_should_return_permission_given_valid_name(self):
        permission = Permission.search("Test")

        self.assertEqual(permission, self.permission)

    def test_should_return_none_given_invalid_name(self):
        permission = Permission.search("Non existent permission_name")

        self.assertEqual(permission, None)
