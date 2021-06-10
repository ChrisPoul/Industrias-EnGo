from datetime import date
from . import Test
from EnGo.calendar import Calendar


class CalendarTest(Test):

    def setUp(self):
        Test.setUp(self)
        

class TestYear(CalendarTest):

    def test_should_return_365_days_given_date_in_normal_year(self):
        calendar = Calendar(date(2020, 1, 1))

        self.asssertEqual(len(calendar.days), 365)