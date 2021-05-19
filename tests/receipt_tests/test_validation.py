from . import ReceiptTest
from EnGo.models.receipt import Receipt


class ReceiptValidationTest(ReceiptTest):

    def setUp(self):
        ReceiptTest.setUp(self)
        self.receipt.add_product(self.product_1)
        self.receipt.add_product(self.product_2)

    
class Validate(ReceiptValidationTest):

    def test_should_not_return_error_given_valid_customer_and_products(self):
        error = self.receipt.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_customer_and_valid_products(self):
        self.customer.customer_name = ""
        error = self.receipt.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_products_and_valid_customer(self):
        self.product_1.code = ""
        error = self.receipt.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_products_and_invalid_customer(self):
        self.customer.customer_name = ""
        self.product_1.code = ""
        error = self.receipt.validation.validate()

        self.assertNotEqual(error, None)


class ValidateCustomer(ReceiptValidationTest):

    def test_should_not_return_error_given_valid_customer(self):
        error = self.receipt.validation.validate_customer()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_customer(self):
        self.customer.customer_name = ""
        error = self.receipt.validation.validate_customer()

        self.assertNotEqual(error, None)


class TestValidateProducts(ReceiptValidationTest):

    def test_should_not_return_error_given_valid_products(self):
        error = self.receipt.validation.validate_products()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_products(self):
        self.product_1.code = ""
        error = self.receipt.validation.validate_products()

        self.assertNotEqual(error, None)
