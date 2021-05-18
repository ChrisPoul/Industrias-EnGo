from . import CustomerTest
from flask import url_for
from EnGo.models.customer import Customer


class TestCustomersView(CustomerTest):

    def test_should_return_valid_response(self):
        with self.client as client:
            response = client.get(
                url_for('customer.customers')
            )
        
        self.assert200(response)


class TestAddView(CustomerTest):

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


class TestUpdateView(CustomerTest):

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
        self.db.session.rollback()
        
        self.assertEqual(self.customer.customer_name, "New Name")

    def test_should_not_update_customer_given_invalid_customer_data(self):
        customer_data = dict(
            customer_name="", 
            address="Valid Address",
            rfc=""
        )
        with self.client as client:
            client.post(
                url_for('customer.update', id=self.customer.id),
                data=customer_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.customer.customer_name, "")

class DeleteCustomerView(CustomerTest):

    def test_should_delete_customer(self):
        with self.client as client:
            client.get(
                url_for('customer.delete', id=self.customer.id)
            )
        
        self.assertNotIn(self.customer, self.db.session)
    
    def test_should_redirect(self):
        with self.client as client:
            response = client.get(
                url_for('customer.delete', id=self.customer.id)
            )

        self.assertStatus(response, 302)


