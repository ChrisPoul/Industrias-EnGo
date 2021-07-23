from datetime import date
from . import OrderTest
from EnGo.models.order import Order


class TestValidate(OrderTest):

    def test_should_not_return_error_given_valid_order(self):
        order = Order(
            user_id=1,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_order(self):
        order = Order(
            user_id=1,
            title="",
            description="Test Description",
            due_date="Invalid date"
        )
        error = order.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(OrderTest):

    def test_should_not_return_error_given_no_empty_values(self):
        order = Order(
            user_id=1,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_title(self):
        order = Order(
            user_id=1,
            title="",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_empty_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_due_date(self):
        order = Order(
            user_id=1,
            title="Test Title",
            description="Test Description",
            due_date=""
        )
        error = order.validation.validate_empty_values()

        self.assertNotEqual(error, None)
