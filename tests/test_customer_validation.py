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
        self.customer.add()


class TestValidate(CustomerValidationTest):

    def test_should_not_return_error_given_valid_customer(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="Unique RFC"
        )
        error = customer.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_value(self):
        customer = Customer(
            customer_name="",
            address="Test Address",
            rfc="Unique RFC"
        )
        error = customer.validation.validate()

        self.assertNotEqual(error, None)
    
    def test_should_return_error_given_repeated_value(self):
        customer = Customer(
            customer_name="Unique Name",
            address="Unique Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate()

        self.assertNotEqual(error, None)

class TestValidateEmptyValues(CustomerValidationTest):

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
    

class TestValidateEmptyValue(CustomerValidationTest):

    def test_should_not_return_error_given_non_empty_name(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate_empty_value("customer_name")

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_name(self):
        customer = Customer(
            customer_name="",
            address="Test Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate_empty_value("customer_name")

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(CustomerValidationTest):

    def test_should_not_return_error_given_unique_rfc(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="Unique RFC"
        )
        error = customer.validation.validate_unique_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_repeated_rfc(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate_unique_values()

        self.assertNotEqual(error, None)


class TestValidateUniqueValue(CustomerValidationTest):

    def test_should_not_return_error_given_unique_name(self):
        customer = Customer(
            customer_name="Unique Name",
            address="Test Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate_unique_value("customer_name")

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_name(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            rfc="TESTRFC 123"
        )
        error = customer.validation.validate_unique_value("customer_name")

        self.assertNotEqual(error, None)