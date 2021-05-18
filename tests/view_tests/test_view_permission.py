from . import ViewTest
from EnGo.models.view import View
from EnGo.models.permission import Permission


class ViewPermissionTest(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.admin_permission = Permission(
            permission_name="admin"
        )
        self.admin_permission.add()
        self.quality_permission = Permission(
            permission_name="quality"
        )
        self.quality_permission.add()


class TestAddPermissions(ViewPermissionTest):

    def test_should_add_permissions_to_view_given_list_of_permissions(self):
        permissions = [self.admin_permission, self.quality_permission]
        self.view.add_permissions(permissions)

        self.assertEqual(self.view.permissions, permissions)


class TestAddPermission(ViewPermissionTest):

    def test_should_add_permission_to_view_given_a_permission_object(self):
        self.view.add_permission(self.admin_permission)

        self.assertIn(self.admin_permission, self.view.permissions)


class TestUpdatePermissions(ViewPermissionTest):

    def setUp(self):
        ViewPermissionTest.setUp(self)
        self.view.add_permission(self.admin_permission)

    def test_should_update_view_permissions_given_list_of_permissions(self):
        permissions = [self.admin_permission, self.quality_permission]
        self.view.update_permissions(permissions)

        self.assertEqual(self.view.permissions, permissions)


class TestDeletePermissions(ViewPermissionTest):

    def setUp(self):
        ViewPermissionTest.setUp(self)
        permissions = [self.admin_permission, self.quality_permission]
        self.view.add_permissions(permissions)

    def test_should_delete_all_view_permissions(self):
        self.view.delete_permissions()

        self.assertEqual(len(self.view.permissions), 0)