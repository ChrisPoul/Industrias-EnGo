from . import Test
from flask import url_for
from EnGo.models.user import User, UserPermission
from EnGo.models.permission import Permission


class AdminViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.admin_user = User(
            username="Admin User",
            password="0000"
        )
        self.admin_user.add()
        self.permission = Permission(
            permission_name="admin",
        )
        self.permission.add()
        user_permission = UserPermission(
            user_id=self.admin_user.id,
            permission_id=self.permission.id
        )
        user_permission.add()
        self.normal_user = User(
            username="Normal User",
            password="0000"
        )
        self.normal_user.add()


class TestMainPage(AdminViewTest):

    def test_should_grant_access_given_loged_in_user_is_admin(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.admin_user.id
        response = self.client.get(
            url_for('admin.main_page')
        )

        self.assert200(response)

    def test_should_return_redirect_given_loged_in_user_is_not_admin(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for('admin.main_page')
        )

        self.assertStatus(response, 302)
