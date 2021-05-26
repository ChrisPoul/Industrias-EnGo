from tests import Test
from EnGo.models.user import User
from EnGo.models.view import View


class AdminTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test User",
            password="0000"
        )
        self.user.add()
        self.view = View(
            view_name="Test View"
        )
        self.view.add()