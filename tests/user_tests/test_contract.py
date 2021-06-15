from datetime import datetime, timedelta
from . import UserTest
from EnGo.models.user.contract import Contract, get_elapsed_time


class TestContract(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        contract = Contract(
            user_id=self.user.id,
            type="Contract Type",
            start=datetime(2020, 1, 1),
            end=datetime(2021, 1, 1)
        )
        contract.add()
    

class TestDuration(TestContract):

    def test_should_return_duration_in_days_given_contract_end_date(self):
        self.user.contract.start = datetime(2021, 1, 1)
        self.user.contract.end = datetime(2021, 1, 10)

        self.assertEqual(self.user.contract.duration, 9)

    def test_should_return_none_given_indefinite_contract(self):
        self.user.contract.end = None

        self.assertEqual(self.user.contract.duration, None)


class TestSeniority(TestContract):

    def test_should_return_days_passed_since_start_of_contract_up_to_today(self):
        start_date = datetime(2021, 6, 1)
        self.user.contract.start = start_date
        elapsed_time_up_to_today = datetime.today() - start_date

        self.assertEqual(self.user.contract.seniority, elapsed_time_up_to_today.days)


class VacationDays(TestContract):

    def test_should_return_6_days_given_less_than_a_year_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=360)
        
        self.assertEqual(self.user.contract.vacation_days, 6)

    def test_should_return_12_given_four_years_or_less_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=4*360)
        
        self.assertEqual(self.user.contract.vacation_days, 12)


class TestGetElapsedTime(TestContract):

    def test_should_return_years_elapsed_between_two_dates_given_years_as_parameter(self):
        elapsed_years = get_elapsed_time(datetime(2020, 1, 1), datetime(2020, 12, 30), "years")

        self.assertEqual(elapsed_years, 0)

    def test_should_return_months_elapsed_between_two_dates_given_months_as_parameter(self):
        
