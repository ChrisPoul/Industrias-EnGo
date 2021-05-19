from . import ReceiptTest
from EnGo.models.receipt import Receipt
from EnGo.models.customer import Customer
from flask import url_for


class ReceiptViewTest(ReceiptTest):

    def setUp(self):
        ReceiptTest.setUp(self)
        self.create_test_users()


class TestAddView(ReceiptViewTest):

    def test_should_add_receipt_given_valid_customer_data(self):
        customer_data = dict(
            customer_name="Test Name",
            address="Test Address",
            rfc="Test RFC"
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for("receipt.add"),
                data=customer_data
            )

        self.assertNotEqual(len(Receipt.get_all()), len(prev_receipts))
    
    def test_should_not_add_receipt_given_invalid_customer_data(self):
        customer_data = dict(
            customer_name="",
            address="Invalid Address",
            rfc="Invalid RFC"
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for('receipt.add'),
                data=customer_data
            )
    
        self.assertEqual(len(Receipt.get_all()), len(prev_receipts))
    
    def test_should_add_receipt_and_new_customer_given_valid_customer_data(self):
        customer_data = dict(
            customer_name="Valid New Name",
            address="Valid Address",
            rfc="Valid RFC"
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for('receipt.add'),
                data=customer_data
            )
        
        self.assertNotEqual(len(Receipt.get_all()), len(prev_receipts))
        self.assertEqual(len(Customer.search('Valid New Name')), 1)

    def test_should_redirect_given_valid_customer_data(self):
        customer_data = dict(
            customer_name="Valid New Name",
            address="Valid Address",
            rfc="Valid RFC"
        )
        with self.client as client:
            response = client.post(
                url_for('receipt.add'),
                data=customer_data
            )
        
        self.assertStatus(response, 302)


class TestEditView(ReceiptViewTest):

    def test_should_update_receipt_customer_given_valid_customer_data(self):
        customer_data = dict(
            customer_name="New Name",
            address="New Address",
            rfc="New RFC"
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=customer_data
            )
        self.db.session.rollback()

        self.assertEqual(self.customer.customer_name, 'New Name')
