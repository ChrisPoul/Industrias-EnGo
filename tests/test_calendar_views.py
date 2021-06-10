from flask import url_for
from . import Test

### LOGED IN USER (LU) ###


class CalendarViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.create_test_users()


class TestCalendarView(CalendarViewTest):

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


class TestDayView(CalendarViewTest):

    def test_should_return_valid_response_given_valid_date_string_and_LU(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('calendar.day', date_str="30.12.2020")
            )
        
        self.assert200(response)

    def test_should_redirect_given_no_LU(self):
        with self.client as client:
            response = client.get(
                url_for('calendar.day', date_str="30.12.2020")
            )
        
        self.assertStatus(response, 302)