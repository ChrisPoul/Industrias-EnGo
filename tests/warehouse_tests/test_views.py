from flask import url_for
from . import WarehouseTest
from EnGo.models.warehouse import Warehouse

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class WarehouseViewTest(WarehouseTest):

    def setUp(self):
        WarehouseTest.setUp(self)
        self.create_test_users()


class TestWarehousesView(WarehouseViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            response = client.get(
                url_for('warehouse.warehouses')
            )

        self.assert200(response)

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('warehouse.warehouses')
            )

        self.assertStatus(response, 302)    
    

class TestAddView(WarehouseViewTest):

    def test_should_add_warehouse_given_valid_warehouse_data_and_LUHP(self):
        self.login_user(self.admin_user)
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
        self.login_user(self.admin_user)
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
        self.login_user(self.admin_user)
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
        self.login_user(self.admin_user)
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
        self.login_user(self.admin_user)
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


class TestInventoryView(WarehouseViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
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
