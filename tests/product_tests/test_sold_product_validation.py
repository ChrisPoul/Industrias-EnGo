from . import ProductTest
from EnGo.models.product import SoldProduct


class SoldProductTest(ProductTest):

    def setUp(self):
        ProductTest.setUp(self)
        self.sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity=0,
            unit="pz",
            price=0
        )
        self.sold_product.add()


class TestValidate(SoldProductTest):

    def test_should_not_return_error_given_valid_sold_product(self):
        error = self.sold_product.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_empty_value(self):
        self.sold_product.quantity = ""
        error = self.sold_product.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_num(self):
        self.sold_product.quantity = "invalid num"
        error = self.sold_product.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(SoldProductTest):

    def test_should_not_return_error_given_no_emtpy_values(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity=0,
            unit="pz",
            price=0
        )
        error = sold_product.validation.validate_empty_values()

        self.assertEqual(error, None)

    def test_should_return_error_given_emtpy_price(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity=0,
            unit="pz",
            price=""
        )
        error = sold_product.validation.validate_empty_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_emtpy_quantity(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity="",
            unit="pz",
            price=0
        )
        error = sold_product.validation.validate_empty_values()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_emtpy_unit(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity=0,
            unit="",
            price=0
        )
        error = sold_product.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateNums(SoldProductTest):

    def test_should_not_return_error_given_valid_numbers(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity=0,
            unit="pz",
            price=0
        )
        error = sold_product.validation.validate_nums()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_quantity(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity="invalid quantity",
            unit="pz",
            price=0
        )
        error = sold_product.validation.validate_nums()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_price(self):
        sold_product = SoldProduct(
            product_id=self.product.id,
            receipt_id=1,
            quantity=0,
            unit="pz",
            price="invalid price"
        )
        error = sold_product.validation.validate_nums()

        self.assertNotEqual(error, None)

