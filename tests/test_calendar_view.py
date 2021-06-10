from flask import url_for
from . import Test

### LOGED IN USER (LU) ###


class TestCalendarView(Test):

    def setUp(self):
        Test.setUp(self)
        self.create_test_users()

    def test_should_return_valid_response_given_LU(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('calendar.calendar')
            )
        
        self.assert200(response)

    def test_should_redirect_given_no_LU(self):
        with self.client as client:
            response = client.get(
                url_for('calendar.calendar')
            )

        self.assertStatus(response, 302)
