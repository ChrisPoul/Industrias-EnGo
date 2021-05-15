from .setup import Test
from EnGo.models.permission import Permission
from EnGo.models.user import User, UserPermission
from EnGo.models.view import View, ViewPermission


class UserPermissionTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.admin_permission = Permission(
        name="admin"
        )
        self.admin_permission.add()
        self.quality_permission = Permission(
            name="quality"
        )
        self.quality_permission.add()
        self.view = View(
            name="Test View"
        )
        self.view.add()
        self.view_admin_permission = ViewPermission(
            view_id=self.view.id,
            permission_id=self.admin_permission.id
        )
        self.view_admin_permission.add()
        self.user = User(
            username="Admin User",
            password="0000"
        )
        self.user.add()


class TestHasPermission(UserPermissionTest):

    def test_should_return_true_given_admin_user(self):
        user_permission = UserPermission(
            user_id=self.user.id,
            permission_id=self.admin_permission.id
        )
        user_permission.add()
        
        self.assertTrue(self.user.has_permission())


class TestIsAdmin(UserPermissionTest):

    def test_should_return_true_given_admin_user(self):
        user_permission = UserPermission(
            user_id=self.user.id,
            permission_id=self.admin_permission.id
        )
        user_permission.add()
        
        self.assertTrue(self.user.is_admin())
