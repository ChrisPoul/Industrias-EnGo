from . import Test
from flask import url_for
from EnGo.models.product import Product


class ProductViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()


class TestAddView(ProductViewTest):

    def test_should_add_product_given_valid_product_data(self):
        product_data = dict(
            code="Valid Code",
            description="Some description",
            price="10"
        )
        with self.client as client:
            client.post(
                url_for("product.add"),
                data=product_data
            )

        self.assertEqual(len(Product.get_all()), 2)

    def test_should_not_add_product_given_invalid_product_data(self):
        product_data = dict(
            code="",
            description="Some description",
            price="invalid price"
        )
        with self.client as client:
            client.post(
                url_for("product.add"),
                data=product_data
            )

        self.assertEqual(len(Product.get_all()), 1)


class TestUpdateView(ProductViewTest):

    def test_should_update_product_given_valid_product_data(self):
        product_data = dict(
            code="New Code",
            description="",
            price="20"
        )
        with self.client as client:
            client.post(
                url_for("product.update", id=self.product.id),
                data=product_data
            )
        self.db.rollback()
        
        self.assertEqual(self.product.code, "New Code")
