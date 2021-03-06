from . import FinishedProductTest
from EnGo.models.product import FinishedProduct


class TestValidation(FinishedProductTest):

    def test_should_not_return_error_given_valid_finished_product(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity=1,
            unit="pz"
        )
        error = finished_product.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_invalid_finished_product(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity="",
            unit="pz"
        )
        error = finished_product.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(FinishedProductTest):

    def test_should_not_return_error_given_no_empty_values(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity=1,
            unit="pz"
        )
        error = finished_product.validation.validate_empty_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_quantity(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity="",
            unit="pz"
        )
        error = finished_product.validation.validate_empty_values()

        self.assertNotEqual(error, None)
    
    def test_should_return_error_given_empty_unit(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity="1",
            unit=""
        )
        error = finished_product.validation.validate_empty_values()

        self.assertNotEqual(error, None)
    

class TestValidateNums(FinishedProductTest):

    def test_should_not_return_error_given_valid_quantity(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity=1,
            unit="pz"
        )
        error = finished_product.validation.validate_nums()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_invalid_quantity(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity="Invalid Quantity",
            unit="pz"
        )
        error = finished_product.validation.validate_nums()

        self.assertNotEqual(error, None)
