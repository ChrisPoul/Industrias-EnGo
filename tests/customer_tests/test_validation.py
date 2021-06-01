from . import CustomerTest
from EnGo.models.customer import Customer


class TestValidate(CustomerTest):

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
            rfc="Test RFC"
        )
        error = customer.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_phone(self):
        customer = Customer(
            customer_name="Unique Name",
            address="Unique Address",
            rfc="Unique RFC",
            phone="invalid phone"
        )
        error = customer.validation.validate()

        self.assertNotEqual(error, None)

class TestValidateEmptyValues(CustomerTest):

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


class TestValidateUniqueValues(CustomerTest):

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
            rfc="Test RFC"
        )
        error = customer.validation.validate_unique_values()

        self.assertNotEqual(error, None)

    def test_should_not_return_error_given_customer_already_in_db(self):
        error = self.customer.validation.validate_unique_values()

        self.assertEqual(error, None)

    def test_should_not_return_error_given_two_customers_with_empty_rfc(self):
        self.customer.rfc = ""
        self.customer.update()
        customer = Customer(
            customer_name="Valid Name",
            address="Valid Address",
            rfc=""
        )
        error = customer.validation.validate_unique_values()

        self.assertEqual(error, None)


class TestValidateOptionalUniqueValue(CustomerTest):
    
    def test_should_not_return_error_given_two_customers_with_empty_name(self):
        self.customer.customer_name = ""
        self.customer.update()
        customer = Customer(
            customer_name="",
            address="Valid Address",
            rfc="Test RFC"
        )
        error = customer.validation.validate_optional_unique_value('customer_name')
        
        self.assertEqual(error, None)


class TestValidateUniqueValue(CustomerTest):

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


class TestValidatePhone(CustomerTest):

    def test_should_not_return_error_given_valid_phone(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            phone="+442 303 2121"
        )
        error = customer.validation.validate_phone()

        self.assertEqual(error, None)

    def test_should_not_return_error_given_empty_phone(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            phone=""
        )
        error = customer.validation.validate_phone()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_phone(self):
        customer = Customer(
            customer_name="Test Name",
            address="Test Address",
            phone="invalid phone"
        )
        error = customer.validation.validate_phone()

        self.assertNotEqual(error, None)
