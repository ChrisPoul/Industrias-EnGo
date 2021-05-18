from tests import Test
from EnGo.models.user import User


class UserTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test User",
            password="0000"
        )
        self.user.add()