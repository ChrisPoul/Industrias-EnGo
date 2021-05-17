from . import Test
from EnGo.models.product import Product


class ProductValidationTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()


class TestValidate(ProductValidationTest):
    
    def test_should_not_return_error_given_valid_product(self):
        product = Product(
            code="Valid Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_value(self):
        product = Product(
            code="",
            description="Optional description",
            price=10
        )
        error = product.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_price(self):
        product = Product(
            code="Some Code",
            description="Optional description",
            price="invalid price"
        )
        error = product.validation.validate()

        self.assertNotEqual(error, None)
        
        
class TestValidateEmptyValues(ProductValidationTest):

    def test_should_not_return_error_given_non_empty_value(self):
        product = Product(
            code="Valid Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_value(self):
        product = Product(
            code="",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(ProductValidationTest):

    def test_should_not_return_error_given_unique_value(self):
        product = Product(
            code="Unique Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_unique_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_unique_values()

        self.assertNotEqual(error, None)

    def test_should_not_return_error_given_product_already_in_database(self):
        product = Product(
            code="Unique Code",
            description="Optional description",
            price=10
        )
        product.add()
        error = product.validation.validate_unique_values()

        self.assertEqual(error, None)


class ValidatePrice(ProductValidationTest):

    def test_should_not_return_error_given_valid_price(self):
        product = Product(
            code="Some Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_price()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_price(self):
        product = Product(
            code="Some Code",
            description="Optional description",
            price="invalid price"
        )
        error = product.validation.validate_price()

        self.assertNotEqual(error, None)
