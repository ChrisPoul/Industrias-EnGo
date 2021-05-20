from . import Test
from flask import url_for
from EnGo.models.user import User
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###


class AdminViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.create_test_users()


class TestMainPage(AdminViewTest):

    def test_should_grant_access_given_LU_is_admin(self):
        self.login_user(self.admin_user)
        response = self.client.get(
            url_for('admin.main_page')
        )

        self.assert200(response)

    def test_should_return_redirect_given_LU_is_not_admin(self):
        self.login_user(self.normal_user)
        response = self.client.get(
            url_for('admin.main_page')
        )

        self.assertStatus(response, 302)
