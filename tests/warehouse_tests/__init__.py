from tests import Test
from EnGo.models.warehouse import Warehouse


class WarehouseTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.warehouse = Warehouse(
            name="Test Warehouse"
        )
        self.warehouse.add()
