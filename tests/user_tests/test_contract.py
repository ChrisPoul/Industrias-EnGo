from datetime import datetime
from . import UserTest
from EnGo.models.user import Contract


class TestContract(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.contract = Contract(
            user_id=self.user.id,
            type="Contract Type",
            start=datetime(2020, 1, 1),
            end=datetime(2021, 1, 1)
        )
        self.contract.add()
    

class TestDuration(TestContract):

    def test_should_return_duration_in_days_given_start_and_end_dates(self):
        self.contract.start = datetime(2021, 1, 1)
        self.contract.end = datetime(2021, 1, 2)
        self.assertEqual(self.user.contract.duration, 1)
