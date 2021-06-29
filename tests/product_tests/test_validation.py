from . import ProductTest
from EnGo.models.product import Product


class TestValidate(ProductTest):
    
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
        
        
class TestValidateEmptyValues(ProductTest):

    def test_should_not_return_error_given_non_empty_value(self):
        product = Product(
            code="Valid Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_code(self):
        product = Product(
            code="",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_empty_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_empty_price(self):
        product = Product(
            code="Valid Code",
            description="Optional description",
            price=""
        )
        error = product.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(ProductTest):

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
            warehouse_id=1,
            code="Unique Code",
            description="Optional description",
            price=10
        )
        product.add()
        error = product.validation.validate_unique_values()

        self.assertEqual(error, None)


class TestValidateNums(ProductTest):

    def test_should_not_return_error_given_valid_nums(self):
        product = Product(
            code="Some Code",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_nums()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_price(self):
        product = Product(
            code="Some Code",
            description="Optional description",
            price="invalid price"
        )
        error = product.validation.validate_nums()

        self.assertNotEqual(error, None)
