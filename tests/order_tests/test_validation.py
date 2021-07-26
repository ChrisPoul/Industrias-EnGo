from datetime import date
from . import OrderTest
from EnGo.models.order import Order


class TestValidate(OrderTest):

    def test_should_not_return_error_given_valid_order(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_value_order(self):
        order = Order(
            user_id=self.user.id,
            title="",
            description="Test Description",
            due_date="Invalid date"
        )
        error = order.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_user_id(self):
        order = Order(
            user_id=0,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_due_date(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date="invalid date format"
        )
        error = order.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(OrderTest):

    def test_should_not_return_error_given_no_empty_values(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_title(self):
        order = Order(
            user_id=self.user.id,
            title="",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateUser(OrderTest):

    def test_should_not_return_error_given_valid_user_id(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_user()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_user_id(self):
        order = Order(
            user_id=0,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_user()

        self.assertNotEqual(error, None)


class TestValidateDueDate(OrderTest):

    def test_should_not_return_error_given_valid_due_date_str_format(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date=date.today()
        )
        error = order.validation.validate_due_date()

        self.assertEqual(error, None)

    def test_should_not_return_error_given_valid_due_date_str_format(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date="2021-06-30"
        )
        error = order.validation.validate_due_date()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_due_date_str_format(self):
        order = Order(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date="invalid date format"
        )
        error = order.validation.validate_due_date()

        self.assertNotEqual(error, None)
