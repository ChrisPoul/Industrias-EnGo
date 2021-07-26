from datetime import date
from . import OrderTest
from EnGo.models.order import Order


class TestAdd(OrderTest):

    def test_should_add_order_given_valid_order(self):
        order = Order(
            user_id=1,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        order.request.add()

        self.assertIn(order, self.db.session)

    def test_should_not_add_order_given_invalid_order(self):
        order = Order(
            user_id=1,
            title="",
            description="Test Description",
            due_date="Invalid date"
        )
        order.request.add()

        self.assertNotIn(order, self.db.session)


class TestUpdate(OrderTest):

    def test_should_update_order_given_valid_changes(self):
        self.order.title = "New Valid Title"
        self.order.request.update()
        self.db.session.rollback()

        self.assertEqual(self.order.title, "New Valid Title")

    def test_should_update_order_given_valid_due_date_str_format(self):
        self.order.due_date = date.today().strftime("%Y-%m-%d")
        self.order.request.update()
        self.db.session.rollback()

        self.assertEqual(self.order.due_date, date.today())
