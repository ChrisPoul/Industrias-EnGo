from . import AdminTest
from flask import url_for
from EnGo.models.user import User
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###


class AdminViewTest(AdminTest):

    def setUp(self):
        AdminTest.setUp(self)
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
    
    def test_should_redirect_given_valid_user_search_term(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Test User"
        )
        with self.client as client:
            response = client.post(
                url_for('admin.main_page'),
                data=search_data
            )
        
        self.assertStatus(response, 302)

    def test_should_redirect_given_valid_view_search_term(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Test View"
        )
        with self.client as client:
            response = client.post(
                url_for('admin.main_page'),
                data=search_data
            )
        
        self.assertStatus(response, 302)

    def test_should_not_redirect_given_invalid_search_term(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Invalid term"
        )
        with self.client as client:
            response = client.post(
                url_for('admin.main_page'),
                data=search_data
            )
        
        self.assert200(response)
