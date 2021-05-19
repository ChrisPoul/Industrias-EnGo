from . import ReceiptTest
from datetime import datetime
from EnGo.models.receipt import Receipt


class TestAdd(ReceiptTest):

    def test_should_add_receipt(self):
        receipt = Receipt(
            customer_id=self.customer.id
        )
        receipt.add()

        self.assertIn(receipt, self.db.session)


class TestUpdate(ReceiptTest):

    def test_should_update_receipt(self):
        old_date = self.receipt.date
        self.receipt.date = datetime.now()
        self.receipt.update()
        self.db.session.rollback()

        self.assertNotEqual(self.receipt.date, old_date)


class TestDelete(ReceiptTest):

    def test_should_delete_receipt(self):
        self.receipt.delete()

        self.assertNotIn(self.receipt, self.db.session)


class TestGet(ReceiptTest):

    def test_should_return_receipt_given_valid_id(self):
        receipt = Receipt.get(self.receipt.id)

        self.assertEqual(receipt, self.receipt)

    def test_should_return_none_given_invalid_id(self):
        receipt = Receipt.get(100)

        self.assertEqual(receipt, None)


class TestGetAll(ReceiptTest):

    def test_should_return_list_of_all_receipts(self):
        receipts = Receipt.get_all()

        self.assertEqual(receipts, [self.receipt])


class TestAddProduct(ReceiptTest):

    def test_should_add_product_to_receipt(self):
        self.receipt.add_product(self.product_1)

        self.assertEqual(self.receipt.products, [self.product_1])
