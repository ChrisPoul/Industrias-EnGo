from . import CustomerTest
from EnGo.models.customer import Customer


class TestAdd(CustomerTest):
    
    def test_should_add_customer(self):
        customer = Customer(
            customer_name="Test Customer",
            address="Test dirección",
            rfc="Opcional RFC"
        )
        customer.add()

        self.assertIn(customer, self.db.session)


class TestUpdate(CustomerTest):

    def test_should_update_customer(self):
        self.customer.customer_name = "New Name"
        self.customer.update()
        self.db.session.rollback()

        self.assertEqual(self.customer.customer_name, "New Name")


class TestDelete(CustomerTest):

    def test_should_delete_customer(self):
        self.customer.delete()
        
        self.assertNotIn(self.customer, self.db.session)


class TestGet(CustomerTest):

    def test_should_return_customer_given_valid_id(self):
        customer = Customer.get(self.customer.id)

        self.assertEqual(customer, self.customer)
    
    def test_should_return_none_given_invalid_id(self):
        customer = Customer.get(2)

        self.assertEqual(customer, None)


class TestGetAll(CustomerTest):

    def test_should_return_list_of_all_customers(self):
        customers = Customer.get_all()

        self.assertEqual(customers, [self.customer])


class TestSearch(CustomerTest):

    def test_should_return_list_of_customers_given_valid_name(self):
        customers = Customer.search(self.customer.customer_name)

        self.assertEqual(customers, [self.customer])
    
    def test_should_return_list_of_customers_given_valid_address(self):
        customers = Customer.search(self.customer.address)

        self.assertEqual(customers, [self.customer])
    
    def test_should_return_list_of_customers_given_valid_rfc(self):
        customers = Customer.search(self.customer.rfc)

        self.assertEqual(customers, [self.customer])
    
    def test_should_return_empty_list_given_invalid_search_term(self):
        customer = Customer.search("invalid search term")

        self.assertEqual(customer, [])
    


