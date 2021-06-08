from . import WarehouseTest
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense
from EnGo.models.product import Product


class TestAdd(WarehouseTest):

    def test_sould_add_warehouse_given_valid_warehouse(self):
        warehouse = Warehouse(
            address="Valid Address"
        )
        warehouse.request.add()

        self.assertIn(warehouse, self.db.session)

    def test_should_not_add_warehouse_given_invalid_warehouse(self):
        warehouse = Warehouse(
            address=""
        )
        warehouse.request.add()
        
        self.assertNotIn(warehouse, self.db.session)


class TestUpdate(WarehouseTest):

    def test_should_update_warehouse_given_valid_changes(self):
        self.warehouse.address = "New Address"
        self.warehouse.request.update()
        self.db.session.rollback()

        self.assertEqual(self.warehouse.address, "New Address")
    
    def test_should_not_update_warehouse_given_invalid_changes(self):
        self.warehouse.address = ""
        self.warehouse.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.warehouse.address, "")


class TestAddExpense(WarehouseTest):

    def test_should_add_expense_to_warehouse_given_existing_expense(self):
        self.warehouse.request.add_expense(self.expense)

        self.assertIn(self.expense, self.warehouse.expenses)
    
    def test_should_add_and_create_expense_given_valid_new_expense(self):
        expense = Expense(
            concept="New Name",
            type_id=1
        )
        self.warehouse.request.add_expense(expense)

        self.assertIn(expense, self.warehouse.expenses)

    def test_should_not_add_expense_to_warehouse_given_invalid_expense(self):
        expense = Expense(
            concept="",
            type_id=1
        )
        self.warehouse.request.add_expense(expense)

        self.assertNotIn(expense, self.warehouse.expenses)
    

