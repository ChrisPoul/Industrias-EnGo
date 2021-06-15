from datetime import datetime
from . import UserTest
from EnGo.models.user import Contract


class TestContract(UserTest):

    def setUp(self, UserTest):
        UserTest.setUp(self)
        self.contract = Contract(
            user_id=self.user.id,
            type="Contract Type",
            start=datetime(2021, 1, 1),
            end=datetime(2022, 1, 1)
        )
        self.contract.add()
    

class TestDuration(TestContract):

    def test_should_return_contract_duration_given_specific_start_and_end(self):
        
        self.assertEqual(self.contract.duration, 36)
