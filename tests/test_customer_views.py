from . import Test
from flask import url_for
from EnGo.models.customer import Customer


class CustomerViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="Test RFC"
        )
        self.customer.add()


class TestAddView(CustomerViewTest):

    def test_should_add_customer_given_valid_customer_data(self):
        customer_data = dict(
            customer_name="Valid Name",
            address="Valid Address",
            rfc=""
        )
        with self.client as client:
            client.post(
                url_for('customer.add'),
                data=customer_data
            )

        self.assertEqual(len(Customer.get_all()), 2)
    
    def test_should_not_add_customer_given_invalid_customer_data(self):
        customer_data = dict(
            customer_name="",
            address="Valid Address",
            rfc=""
        )
        with self.client as client:
            client.post(
                url_for('customer.add'),
                data=customer_data
            )
        
        self.assertEqual(len(Customer.get_all()), 1)


class TestUpdateView(CustomerViewTest):

    def test_should_update_customer_given_valid_customer_data(self):
        customer_data = dict(
            customer_name="New Name", 
            address="Valid Address",
            rfc=""
        )
        with self.client as client:
            client.post(
                url_for('customer.update', id=self.customer.id),
                data=customer_data
            )
        
        self.assertEqual(self.customer.customer_name, "New Name")

