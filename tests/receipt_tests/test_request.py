from . import ReceiptTest
from EnGo.models.receipt import Receipt
from EnGo.models.product import Product


class TestEdit(ReceiptTest):

    def test_should_update_customer_given_valid_customer_and_valid_products(self):
        self.receipt.add_product(self.product_1)
        self.receipt.customer.customer_name = "New Name"
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertEqual(self.receipt.customer.customer_name, "New Name")

    def test_should_not_update_customer_given_invalid_customer_and_valid_products(self):
        self.receipt.add_product(self.product_1)
        self.receipt.customer.customer_name = ""
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.receipt.customer.customer_name, "")
    
    def test_should_not_update_customer_given_valid_customer_and_invalid_products(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = ""
        self.receipt.customer.customer_name = "New Name"
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.receipt.customer.customer_name, "New Name")
    
    def test_should_update_products_given_valid_customer_and_valid_products(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = "New Code"
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertEqual(self.product_1.code, "New Code")
    
    def test_should_not_update_products_given_invalid_products_and_valid_customer(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = ""
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.product_1.code, "")

    def test_should_not_update_products_given_valid_products_and_invalid_customer(self):
        self.receipt.add_product(self.product_1)
        self.product_1.code = "New Code"
        self.receipt.customer.customer_name = ""
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.product_1.code, "New Code")

    def test_should_not_update_given_invalid_sold_product(self):
        self.receipt.add_product(self.product_1)
        sold_product = self.receipt.sold_products[0]
        sold_product.quantity = ""
        self.receipt.request.update()
        self.db.session.rollback()

        self.assertNotEqual(sold_product.quantity, "")
