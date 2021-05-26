from . import CustomerTest
from flask import url_for
from EnGo.models.customer import Customer

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class CustomerViewTest(CustomerTest):

    def setUp(self):
        CustomerTest.setUp(self)
        self.create_test_users()


class TestCustomersView(CustomerViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            response = client.get(
                url_for('customer.customers')
            )
        
        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.customers')
            )
        
        self.assertStatus(response, 302)

    def test_should_not_redirect_given_valid_search_term_and_LUHP(self):
        self.login_user(self.accounting_user)
        search_data = dict(
            search_term="Test Name"
        )
        with self.client as client:
            response = client.post(
                url_for('customer.customers'),
                data=search_data
            )

        self.assert200(response)

    def test_should_not_redirect_given_invalid_search_term_and_LUHP(self):
        self.login_user(self.accounting_user)
        search_data = dict(
            search_term="Invalid search term"
        )
        with self.client as client:
            response = client.post(
                url_for('customer.customers'),
                data=search_data
            )

        self.assert200(response)


class TestAddView(CustomerViewTest):

    def test_should_add_customer_given_valid_customer_data_and_LUHP(self):
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
    
    def test_should_not_add_customer_given_invalid_customer_data_and_LUHP(self):
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

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.add')
            )

        self.assertStatus(response, 302)


class TestUpdateView(CustomerViewTest):

    def test_should_update_customer_given_valid_customer_data_and_LUHP(self):
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

    def test_should_not_update_customer_given_invalid_customer_data_and_LUHP(self):
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

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.update', id=self.customer.id)
            )
        
        self.assertStatus(response, 302)


class DeleteCustomerView(CustomerViewTest):

    def test_should_delete_customer_given_LUHP(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            client.get(
                url_for('customer.delete', id=self.customer.id)
            )
        
        self.assertNotIn(self.customer, self.db.session)

    def test_should_redirect_and_not_delete_customer_given_LUHNP(self):
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


class TestReceiptsView(CustomerViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            response = client.get(
                url_for('customer.receipts', id=self.customer.id)
            )
        
        self.assert200(response)
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('customer.receipts', id=self.customer.id)
            )

        self.assertStatus(response, 302)