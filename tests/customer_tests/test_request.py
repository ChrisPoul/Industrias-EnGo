from . import CustomerTest
from EnGo.models.customer import Customer


class TestAdd(CustomerTest):

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


class TestUpdate(CustomerTest):

    def setUp(self):
        CustomerTest.setUp(self)
        self.customer2 = Customer(
            customer_name="Name Two",
            address="Address Two",
            rfc="RFC Two"
        )
        self.customer2.add()

    def test_should_update_customer_given_valid_change(self):
        self.customer.customer_name = "New Name"
        self.customer.request.update()
        self.db.session.rollback()

        self.assertEqual(self.customer.customer_name, "New Name")

    def test_should_not_update_customer_given_invalid_change(self):
        self.customer2.rfc = "Test RFC"
        self.customer2.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.customer2.rfc, "Test RFC")