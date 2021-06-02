from . import PermissionTest
from EnGo.models.permission import Permission


class TestAdd(PermissionTest):

    def test_should_add_permission(self):
        permission = Permission(
            permission_name="Some Permission"
        )
        permission.add()

        self.assertIn(permission, self.db.session)


class TestUpdate(PermissionTest):

    def test_should_update_permission(self):
        self.admin_permission.permission_name = "New permission_name"
        self.admin_permission.update()
        self.db.session.rollback()

        self.assertEqual(self.admin_permission.permission_name, "New permission_name")


class TestDelete(PermissionTest):

    def test_should_delete_permission(self):
        self.admin_permission.delete()

        self.assertNotIn(self.admin_permission, self.db.session)


class TestGet(PermissionTest):

    def test_should_return_permission_given_valid_id(self):
        permission = Permission.get(1)

        self.assertEqual(permission, self.admin_permission)

    def test_should_return_none_given_invalid_id(self):
        permission = Permission.get(2)

        self.assertEqual(permission, None)


class TestGetAll(PermissionTest):

    def setUp(self):
        PermissionTest.setUp(self)
        self.quality_permission = Permission(
            permission_name="quality"
        )
        self.quality_permission.add()

    def test_should_return_list_of_all_users(self):
        permissions = Permission.get_all()

        self.assertEqual(permissions, [self.admin_permission, self.quality_permission])


class TestSearch(PermissionTest):

    def test_should_return_permission_given_valid_name(self):
        permission = Permission.search("Admin")

        self.assertEqual(permission, self.admin_permission)

    def test_should_return_none_given_invalid_name(self):
        permission = Permission.search("Non existent permission_name")

        self.assertEqual(permission, None)
