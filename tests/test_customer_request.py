from . import Test
from EnGo.models.customer import Customer


class CustomerRequestTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="Test RFC"
        )
        self.customer.add()


class TestAdd(CustomerRequestTest):

    def test_should_add_customer_given_valid_customer(self):
        customer = Customer(
            customer_name="Valid Name",
            address="Valid Address",
            rfc="Valid RFC"
        )
        customer.request.add()

        self.assertIn(customer, self.db.session)

    def test_should_not_add_customer_given_invalid_customer(self):
        customer = Customer(
            customer_name="",
            address="Valid Address",
            rfc="Valid RFC"
        )
        customer.request.add()

        self.assertNotIn(customer, self.db.session)


class TestRequestUpdate(CustomerRequestTest):

    def test_should_update_customer_given_valid_change(self):
        self.customer.customer_name = "New Name"
        self.customer.request.update()

        changed_name = self.customer.customer_name

        self.assertEqual(changed_name, "New Name")