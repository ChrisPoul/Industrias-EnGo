from datetime import date
from tests import Test
from EnGo.models.order import Order
from EnGo.models.user import User


class OrderTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test User",
            password="0000"
        )
        self.user.add()
        self.order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        self.order.add()
