from . import CustomerTest
from flask import url_for
from EnGo.models.customer import Customer


class CustomerViewTest(CustomerTest):

    def setUp(self):
        CustomerTest.setUp(self)
        self.create_test_users()


class TestCustomersView(CustomerViewTest):

    def test_should_return_valid_response_given_logged_in_user_has_permission(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            response = client.get(
                url_for('customer.customers')
            )
        
        self.assert200(response)

    def test_should_redirect_given_logged_in_user_does_not_have_permission(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.customers')
            )
        
        self.assertStatus(response, 302)


class TestAddView(CustomerViewTest):

    def test_should_add_customer_given_valid_customer_data_and_logged_in_user_has_permission(self):
        self.login_user(self.accounting_user)
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
    
    def test_should_not_add_customer_given_invalid_customer_data_and_logged_in_user_has_permission(self):
        self.login_user(self.accounting_user)
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

    def test_should_redirect_given_logged_in_user_does_not_have_permission(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.add')
            )

        self.assertStatus(response, 302)


class TestUpdateView(CustomerViewTest):

    def test_should_update_customer_given_valid_customer_data_and_logged_in_user_has_permission(self):
        self.login_user(self.accounting_user)
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

    def test_should_not_update_customer_given_invalid_customer_data_and_logged_in_user_has_permission(self):
        self.login_user(self.accounting_user)
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

    def test_should_redirect_given_logged_in_user_does_not_have_permission(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.update', id=self.customer.id)
            )
        
        self.assertStatus(response, 302)


class DeleteCustomerView(CustomerViewTest):

    def test_should_delete_customer_given_logged_in_user_has_permission(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            client.get(
                url_for('customer.delete', id=self.customer.id)
            )
        
        self.assertNotIn(self.customer, self.db.session)

    def test_should_redirect_and_not_delete_customer_given_loged_in_user_does_not_have_permission(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.delete', id=self.customer.id)
            )

        self.assertStatus(response, 302)

    def test_should_redirect(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.delete', id=self.customer.id)
            )

        self.assertStatus(response, 302)


