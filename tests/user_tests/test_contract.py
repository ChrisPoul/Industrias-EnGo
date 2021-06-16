from datetime import datetime, timedelta
from . import UserTest
from EnGo.models.user.contract import Contract, get_elapsed_years


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

    def test_should_return_0_given_less_than_a_year_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=364)
        
        self.assertEqual(self.user.contract.vacation_days, 0)

    def test_should_return_6_given_a_year_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=370)
        
        self.assertEqual(self.user.contract.vacation_days, 6)

    def test_should_return_12_given_four_years_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=4*370)
        
        self.assertEqual(self.user.contract.vacation_days, 12)
    
    def test_should_return_14_given_nine_years_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=9*370)

        self.assertEqual(self.user.contract.vacation_days, 14)

    def test_should_return_16_given_fourteen_years_since_start_of_contract(self):
        self.user.contract.start = datetime.today() - timedelta(days=14*370)

        self.assertEqual(self.user.contract.vacation_days, 16)


class TestVacationBonus(TestContract):
    
    def test_should_return_2500_given_3_years_of_seniority_and_a_30_000_salary(self):
        self.user.salary = 30_000
        self.user.contract.start = datetime.today() - timedelta(days=3*370)

        self.assertEqual(self.user.contract.vacation_bonus, 2500)


class TestChristmasBonus(TestContract):

    def test_should_return_15_000_given_monthly_salary_of_30_000(self):
        self.user.salary = 30_000
        
        self.assertEqual()


class TestGetElapsedYears(TestContract):

    def test_should_return_0_given_two_dates_in_different_years_but_less_than_one_year_appart(self):
        elapsed_years = get_elapsed_years(datetime(2020, 12, 1), datetime(2021, 1, 1))

        self.assertEqual(elapsed_years, 0)

    def test_should_return_1_given_two_dates_in_different_years_one_year_appart(self):
        elapsed_years = get_elapsed_years(datetime(2020, 12, 1), datetime(2022, 1, 1))

        self.assertEqual(elapsed_years, 1)

    def test_should_2_given_two_dates_exactly_two_years_appart(self):
        elapsed_years = get_elapsed_years(datetime(2018, 1, 1), datetime(2020, 1, 1))
        
        self.assertEqual(elapsed_years, 2)


