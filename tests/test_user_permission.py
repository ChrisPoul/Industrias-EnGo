from . import Test
from EnGo.models.permission import Permission
from EnGo.models.user import User
from EnGo.models.view import View


class UserPermissionTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.admin_permission = Permission(
        permission_name="admin"
        )
        self.admin_permission.add()
        self.admin_view = View(
            view_name="Admin View"
        )
        self.admin_view.add()
        self.admin_view.add_permission(self.admin_permission)
        self.admin_user = User(
            username="Admin User",
            password="0000"
        )
        self.admin_user.add()
        self.admin_user.add_permission(self.admin_permission)
        self.quality_permission = Permission(
            permission_name="quality"
        )
        self.quality_permission.add()
        self.quality_view = View(
            view_name="Quality View"
        )
        self.quality_view.add()
        self.quality_view.add_permission(self.quality_permission)
        self.normal_user = User(
            username="Normal User",
            password="0000"
        )
        self.normal_user.add()


class TestAddPermission(UserPermissionTest):

    def test_shoul_add_permission_to_user(self):
        user = User(
            username="Quality Manager",
            password="0000"
        )
        user.add()
        user.add_permission(self.quality_permission)

        self.assertIn(self.quality_permission, user.permissions)


class TestHasPermission(UserPermissionTest):

    def test_should_return_true_given_admin_user_and_admin_view(self):
        self.assertTrue(self.admin_user.has_permission("Admin View"))

    def test_should_return_true_given_admin_user_and_any_view(self):        
        self.assertTrue(self.admin_user.has_permission("Quality View"))

    def test_should_return_false_given_normal_user_and_admin_view(self):
        self.assertFalse(self.normal_user.has_permission("Admin View"))

    def test_should_return_true_given_normal_user_with_permissions_required_for_view(self):
        self.normal_user.add_permission(self.quality_permission)

        self.assertTrue(self.normal_user.has_permission("Quality View"))

    
class TestHasViewPermissions(UserPermissionTest):

    def test_should_return_true_given_admin_user_and_admin_view(self):
        self.assertTrue(self.admin_user.has_view_permissions("Admin View"))

    def test_should_return_false_given_admin_user_and_non_admin_view(self):
        self.assertFalse(self.admin_user.has_view_permissions("Quality View"))

    def test_should_return_true_given_user_with_permissions_required_for_view(self):
        self.normal_user.add_permission(self.quality_permission)

        self.assertTrue(self.normal_user.has_view_permissions("Quality View"))

    def test_should_return_false_given_user_without_permissions_required_for_view(self):
        self.assertFalse(self.normal_user.has_view_permissions("Admin View"))


class TestIsAdmin(UserPermissionTest):

    def test_should_return_true_given_admin_user(self):
        self.assertTrue(self.admin_user.is_admin())

    def test_should_return_false_given_normal_user(self):
        self.assertFalse(self.normal_user.is_admin())
