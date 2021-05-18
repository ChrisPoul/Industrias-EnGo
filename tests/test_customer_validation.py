from . import Test
from EnGo.models.customer import Customer


class CustomerValidationTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="TESTRFC 123"
        )


class TestCustomerValidateEmptyValues(CustomerValidationTest):

    def test_should_not_return_error_given_no_empty_values(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc=""
        )
        error = customer.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_name(self):
        customer = Customer(
            customer_name="",
            address="Test Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate_empty_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_address(self):
        customer = Customer(
            customer_name="Test Name",
            address="",
            rfc="Test rfc"
        )
        error = customer.validation.validate_empty_values()

        self.assertNotEqual(error, None)
    
    def test_should_not_return_error_given_empty_rfc(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc=""
        )
        error = customer.validation.validate_empty_values()

        self.assertEqual(error, None)
    

