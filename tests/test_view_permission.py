from .setup import Test
from EnGo.models.view import View, ViewPermission
from EnGo.models.permission import Permission


class ViewPermissionTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.permission1 = Permission(
            permission_name="Permission 1"
        )
        self.permission1.add()
        self.permission2 = Permission(
            permission_name="Permission 2"
        )
        self.permission2.add()
        self.view = View(
            view_name="Test View"
        )
        self.view.add()


class TestAddPermissions(ViewPermissionTest):

    def test_should_add_permissions_to_view_given_list_of_permissions(self):
        permissions = [self.permission1, self.permission2]
        self.view.add_permissions(permissions)

        self.assertEqual(self.view.permissions, permissions)


class TestAddPermission(ViewPermissionTest):

    def test_should_add_permission_to_view_given_a_permission_object(self):
        self.view.add_permission(self.permission1)

        self.assertEqual(self.view.permissions, [self.permission1])


class TestUpdatePermissions(ViewPermissionTest):

    def setUp(self):
        ViewPermissionTest.setUp(self)
        view_permission = ViewPermission(
            view_id=self.view.id,
            permission_id=self.permission1.id
        )
        view_permission.add()

    def test_should_update_view_permissions_given_list_of_permissions(self):
        permissions = [self.permission1, self.permission2]
        self.view.update_permissions(permissions)

        self.assertEqual(self.view.permissions, permissions)


class TestDeletePermissions(ViewPermissionTest):

    def setUp(self):
        ViewPermissionTest.setUp(self)
        view_permission1 = ViewPermission(
            view_id=self.view.id,
            permission_id=self.permission1.id
        )
        view_permission1.add()
        view_permission2 = ViewPermission(
            view_id=self.view.id,
            permission_id=self.permission2.id
        )
        view_permission2.add()

    def test_should_delete_all_view_permissions(self):
        permissions = [self.permission1, self.permission2]
        self.view.delete_permissions()

        self.assertEqual(len(self.view.permissions), 0)