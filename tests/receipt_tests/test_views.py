from . import ReceiptTest
from EnGo.models.receipt import Receipt
from EnGo.models.customer import Customer
from EnGo.models.product import Product
from flask import url_for

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ReceiptViewTest(ReceiptTest):

    def setUp(self):
        ReceiptTest.setUp(self)
        customer2 = Customer(
            customer_name="Name Two",
            address="Address Two",
            rfc=""
        )
        customer2.add()
        self.create_test_users()


class TestAddView(ReceiptViewTest):

    def test_should_add_receipt_given_valid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name="Test Name",
            address="Test Address",
            phone="+123 456 7890"
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for("receipt.add"),
                data=customer_data
            )

        self.assertNotEqual(len(Receipt.get_all()), len(prev_receipts))
    
    def test_should_not_add_receipt_given_invalid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name="",
            address="Invalid Address",
            phone="Invalid Phone"
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for('receipt.add'),
                data=customer_data
            )
    
        self.assertEqual(Receipt.get_all(), prev_receipts)

    def test_should_not_add_receipt_given_empty_values_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name="",
            address="",
            phone=""
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for('receipt.add'),
                data=customer_data
            )
    
        self.assertEqual(Receipt.get_all(), prev_receipts)
    
    def test_should_add_receipt_and_new_customer_given_valid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name="Valid New Name",
            address="Valid Address",
            phone="+123 456 7890"
        )
        prev_receipts = Receipt.get_all()
        with self.client as client:
            client.post(
                url_for('receipt.add'),
                data=customer_data
            )
        
        self.assertNotEqual(len(Receipt.get_all()), len(prev_receipts))
        self.assertEqual(len(Customer.search_all('Valid New Name')), 1)

    def test_should_redirect_given_valid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name="Valid New Name",
            address="Valid Address",
            phone="+123 456 7890"
        )
        with self.client as client:
            response = client.post(
                url_for('receipt.add'),
                data=customer_data
            )
        
        self.assertStatus(response, 302)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('receipt.add')
            )

        self.assertStatus(response, 302)


class TestEditView(ReceiptViewTest):

    def test_should_update_receipt_customer_given_valid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name="New Name"
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=customer_data
            )
        self.db.session.rollback()

        self.assertEqual(self.customer.customer_name, 'New Name')

    def test_should_not_update_customer_given_invalid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        customer_data = dict(
            customer_name=""
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=customer_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.customer.customer_name, '')

    def test_should_update_receipt_products_given_valid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        self.receipt.add_product(self.product_1)
        self.receipt.add_product(self.product_2)
        product_data = dict(
            code_1="New Code",
            code_2="New Code 2"
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=product_data
            )
        self.db.session.rollback()

        self.assertEqual(self.product_1.code, "New Code")
        self.assertEqual(self.product_2.code, "New Code 2")

    def test_should_not_update_receipt_products_given_invalid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        self.receipt.add_product(self.product_1)
        self.receipt.add_product(self.product_2)
        product_data = dict(
            code_1="New Code",
            code_2=""
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=product_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.product_1.code, "New Code")
        self.assertNotEqual(self.product_2.code, "")

    def test_should_not_update_customer_given_valid_customer_data_and_invalid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        self.receipt.add_product(self.product_1)
        data = dict(
            customer_name="New Name",
            code_1=""
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.customer.customer_name, 'New Name')

    def test_should_not_update_receipt_products_given_valid_product_data_and_invalid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        self.receipt.add_product(self.product_1)
        data = dict(
            customer_name="",
            code_1="New Code"
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.product_1.code, 'New Code')

    def test_should_add_product_to_receipt_given_valid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        product_data = dict(
            code="Code 1"
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=product_data
            )
        self.db.session.rollback()

        self.assertIn(self.product_1, self.receipt.products)

    def test_should_create_product_and_add_it_to_receipt_given_valid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        product_data = dict(
            code="New Product",
            description="Some description",
            price=10
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=product_data
            )
        self.db.session.rollback()

        self.assertTrue(Product.search("New Product"))

    def test_should_not_add_product_given_invalid_customer_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        data = dict(
            customer_name="",
            code="Code 1"
        )
        with self.client as client:
            client.post(
                url_for('receipt.edit', id=self.receipt.id),
                data=data
            )
        self.db.session.rollback()

        self.assertNotIn(self.product_1, self.receipt.products)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('receipt.edit', id=self.receipt.id)
            )

        self.assertStatus(response, 302)


class TestDoneView(ReceiptViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            response = client.get(
                url_for('receipt.done', id=self.receipt.id)
            )
        
        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('receipt.done', id=self.receipt.id)
            )

        self.assertStatus(response, 302)


class TestRemoveProduct(ReceiptViewTest):

    def test_should_remove_product_from_receipt_and_LUHP(self):
        self.login_user(self.accounting_user)
        self.receipt.add_product(self.product_1)
        with self.client as client:
            client.get(
                url_for('receipt.remove_product', id=self.product_1.id)
            )

        self.assertNotIn(self.product_1, self.receipt.products)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('receipt.remove_product', id=1)
            )

        self.assertStatus(response, 302)


class TestDeleteView(ReceiptViewTest):

    def test_should_delete_receipt_and_LUHP(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            client.get(
                url_for('receipt.delete', id=self.receipt.id)
            )
        
        self.assertNotIn(self.receipt, self.db.session)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('receipt.delete', id=self.receipt.id)
            )

        self.assertStatus(response, 302)
