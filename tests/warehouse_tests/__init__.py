from tests import Test
from EnGo.models.warehouse import Warehouse
from EnGo.models.expense import Expense
from EnGo.models.product import Product


class WarehouseTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.warehouse = Warehouse(
            address="Test Address"
        )
        self.warehouse.add()
        self.expense = Expense(
            concept="Test Expense",
            type_id=1
        )
        self.expense.add()
        self.product = Product(
            code="Test Product"
        )
        self.product.add()
