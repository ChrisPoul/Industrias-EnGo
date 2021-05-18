from . import ProductTest
from EnGo.models.product import Product


class TestAdd(ProductTest):

    def test_should_add_product_given_valid_product(self):
        product = Product(
            code="Test Code 2",
            price=10
        )
        product.request.add()

        self.assertIn(product, self.db.session)

    def test_should_not_add_product_given_invalid_product(self):
        product = Product(
            code="",
            price=10
        )
        product.request.add()

        self.assertNotIn(product, self.db.session)


class TestUpdate(ProductTest):

    def test_should_update_product_given_valid_product(self):
        self.product.code = "New Code"
        self.product.request.update()
        self.db.session.rollback()

        self.assertEqual(self.product.code, "New Code")

    def test_should_not_update_given_invalid_product(self):
        self.product.price = "invalid price"
        self.product.request.update()
        self.db.session.rollback()

        self.assertEqual(self.product.price, 10)