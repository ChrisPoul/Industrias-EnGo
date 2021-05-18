from . import Test
from flask import url_for
from EnGo.models.user import User


class HomeTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test",
            password="0000"
        )
        self.user.add()



class TestMainPage(HomeTest):

    def test_should_grant_access_given_loged_in_user(self):
        self.login_user(self.user)
        response = self.client.get(
            url_for('home.main_page')
        )

        self.assert200(response)

    def test_should_grant_access_given_no_loged_in_user(self):
        response = self.client.get(
            url_for('home.main_page')
        )

        self.assert200(response)