from datetime import date
from tests import Test
from EnGo.models.order import Order


class OrderTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.order = Order(
            user_id=1,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        self.order.add()
