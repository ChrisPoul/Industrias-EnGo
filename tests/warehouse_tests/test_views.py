from flask import url_for
from . import WarehouseTest
from EnGo.models.warehouse import Warehouse
from EnGo.models.product import Product

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class WarehouseViewTest(WarehouseTest):

    def setUp(self):
        WarehouseTest.setUp(self)
        self.create_test_users()
        self.product = Product(
            warehouse_id=self.warehouse.id,
            code="Test Product",
            description="Test Description",
            price=1
        )
        self.product.add()
    

class TestAddView(WarehouseViewTest):

    def test_should_add_warehouse_given_valid_warehouse_data_and_LUHP(self):
        self.login_user(self.dev_user)
        warehouse_data = dict(
            address="Valid Address"
        )
        with self.client as client:
            client.post(
                url_for('warehouse.add'),
                data=warehouse_data
            )

        self.assertNotEqual(Warehouse.search("Valid Address"), None)

    def test_should_not_add_warehouse_given_invalid_warehouse_data_and_LUHP(self):
        self.login_user(self.dev_user)
        warehouse_data = dict(
            address=""
        )
        with self.client as client:
            client.post(
                url_for('warehouse.add'),
                data=warehouse_data
            )

        self.assertEqual(Warehouse.search(""), None)

    
class TestUpdateView(WarehouseViewTest):

    def test_should_update_warehouse_given_valid_warehouse_data_and_LUHP(self):
        self.login_user(self.dev_user)
        warehouse_data = dict(
            address="Valid Address"
        )
        with self.client as client:
            client.post(
                url_for('warehouse.update', id=self.warehouse.id),
                data=warehouse_data
            )
        self.db.session.rollback()

        self.assertEqual(self.warehouse.address, "Valid Address")

    def test_should_not_update_warehouse_given_invalid_warehouse_data_and_LUHP(self):
        self.login_user(self.dev_user)
        warehouse_data = dict(
            address=""
        )
        with self.client as client:
            client.post(
                url_for('warehouse.update', id=self.warehouse.id),
                data=warehouse_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.warehouse.address, "")


class TestDeleteView(WarehouseViewTest):

    def test_should_delete_warehouse_given_LUHP(self):
        self.login_user(self.dev_user)
        with self.client as client:
            client.get(
                url_for('warehouse.delete', id=self.warehouse.id)
            )
        
        self.assertNotIn(self.warehouse, self.db.session)

    def test_should_not_delete_warehouse_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            client.get(
                url_for('warehouse.delete', id=self.warehouse.id)
            )
        
        self.assertIn(self.warehouse, self.db.session)


class TestAddExpenseView(WarehouseViewTest):

    def test_should_add_expense_to_warehouse_given_valid_expense_input_and_LUHP(self):
        self.login_user(self.dev_user)
        expense_input = dict(
            concept="Test Expense",
            type_id=1,
            cost=10,
            unit="pz",
            quantity=10
        )
        with self.client as client:
            client.post(
                url_for('warehouse.add_expense', id=self.warehouse.id),
                data=expense_input
            )
        
        self.assertEqual(len(self.warehouse.expenses), 1)

    def test_should_not_add_expense_to_warehouse_given_invalid_expense_input_and_LUHP(self):
        self.login_user(self.dev_user)
        expense_input = dict(
            concept="",
            type_id=1,
            cost=10,
            unit="pz",
            quantity=10
        )
        with self.client as client:
            client.post(
                url_for('warehouse.add_expense', id=self.warehouse.id),
                data=expense_input
            )
        
        self.assertEqual(len(self.warehouse.expenses), 0)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('warehouse.add_expense', id=self.warehouse.id)
            )

        self.assertStatus(response, 302)


class TestInventoryView(WarehouseViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.dev_user)
        with self.client as client:
            response = client.get(
                url_for('warehouse.inventory', id=self.warehouse.id)
            )

        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('warehouse.inventory', id=self.warehouse.id)
            )

        self.assertStatus(response, 302)
