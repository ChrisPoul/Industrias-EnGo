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

    def test_should_return_error_given_invalid_product(self):
        product = Product(
            code="",
            description="Optional description",
            price=10
        )
        error = product.validation.validate()

        self.assertNotEqual(error, None)
        
        
class TestValidateEmptyValues(ProductValidationTest):

    def test_should_return_error_given_empty_value(self):
        product = Product(
            code="",
            description="Optional description",
            price=10
        )
        error = product.validation.validate_empty_values()

        self.assertNotEqual(error, None)


