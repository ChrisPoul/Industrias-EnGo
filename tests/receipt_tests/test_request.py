from . import ReceiptTest
from EnGo.models.receipt import Receipt
from EnGo.models.product import Product


class TestEdit(ReceiptTest):

    def test_should_update_customer_given_valid_customer_and_valid_products(self):
        self.receipt.add_product(self.product_1)
        self.receipt.customer.customer_name = "New Name"
        self.receipt.request.edit()
        self.db.session.rollback()

        self.assertEqual(self.receipt.customer.customer_name, "New Name")

    def test_should_not_update_customer_given_invalid_customer_and_valid_products(self):
        self.receipt.add_product(self.product_1)
        self.receipt.customer.customer_name = ""
        self.receipt.request.edit()
        self.db.session.rollback()

        self.assertNotEqual(self.receipt.customer.customer_name, "")
    
    def test_should_not_update_customer_given_valid_customer_and_invalid_products(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = ""
        self.receipt.customer.customer_name = "New Name"
        self.receipt.request.edit()
        self.db.session.rollback()

        self.assertNotEqual(self.receipt.customer.customer_name, "New Name")
    
    def test_should_update_products_given_valid_customer_and_valid_products(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = "New Code"
        self.receipt.request.edit()
        self.db.session.rollback()

        self.assertEqual(self.product_1.code, "New Code")
    
    def test_should_not_update_products_given_invalid_products_and_valid_customer(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = ""
        self.receipt.request.edit()
        self.db.session.rollback()

        self.assertNotEqual(self.product_1.code, "")

    def test_should_not_update_products_given_valid_products_and_invalid_customer(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = "New Code"
        self.receipt.customer.customer_name = ""
        self.receipt.request.edit()
        self.db.session.rollback()

        self.assertNotEqual(self.product_1.code, "New Code")
    
    def test_should_add_products_given_valid_customer_and_valid_products(self):
        product = Product(
            code="Code 2",
            price=10
        )
        self.receipt.add_product(self.product_1)
        self.receipt.request.edit(product)

        self.assertIn(self.product_2, self.receipt.products)


class TestAddProduct(ReceiptTest):

    def test_should_add_product_given_existent_product_values(self):
        product = Product(
            code="Code 1",
            price=20
        )
        self.receipt.request.add_product(product)

        self.assertIn(self.product_1, self.receipt.products)
    
    def test_should_add_product_to_db_and_receipt_given_valid_new_product(self):
        product = Product(
            code="New Code",
            price=20
        )
        self.receipt.request.add_product(product)

        self.assertIn(product, self.db.session)
        self.assertIn(product, self.receipt.products)

    def test_should_not_add_product_to_db_or_receipt_given_invalid_new_product(self):
        product = Product(
            code="",
            price=10
        )
        self.receipt.request.add_product(product)

        self.assertNotIn(product, self.db.session)
        self.assertNotIn(product, self.receipt.products)
    
