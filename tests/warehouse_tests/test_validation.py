from . import WarehouseTest
from EnGo.models.warehouse import Warehouse

from tests import warehouse_tests


class TestValidateEmptyValues(WarehouseTest):

    def test_should_not_return_error_given_valid_warehouse(self):
        warehouse = Warehouse(
            address="Valid Address"
        )
        error = warehouse.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_value(self):
        warehouse = Warehouse(
            address=""
        )
        error = warehouse.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateRepeatedValues(WarehouseTest):

    def test_should_not_return_error_given_valid_warehouse(self):
        warehouse = Warehouse(
            address="Unique Address"
        )
        error = warehouse.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_repeated_value(self):
        warehouse = Warehouse(
            address="Test Address"
        )
        error = warehouse.validation.validate()

        self.assertNotEqual(error, None)