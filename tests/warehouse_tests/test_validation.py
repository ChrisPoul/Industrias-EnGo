from . import WarehouseTest
from EnGo.models.warehouse import Warehouse


class TestValidate(WarehouseTest):

    def test_should_not_return_error_given_valid_warehouse(self):
        warehouse = Warehouse(
            name="Valid name"
        )
        error = warehouse.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_invalid_warehouse(self):
        warehouse = Warehouse(
            name=""
        )
        error = warehouse.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(WarehouseTest):

    def test_should_not_return_error_given_no_empty_values(self):
        warehouse = Warehouse(
            name="Valid name"
        )
        error = warehouse.validation.validate_empty_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_value(self):
        warehouse = Warehouse(
            name=""
        )
        error = warehouse.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateRepeatedValues(WarehouseTest):

    def test_should_not_return_error_given_unique_value(self):
        warehouse = Warehouse(
            name="Unique name"
        )
        error = warehouse.validation.validate_unique_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_repeated_value(self):
        warehouse = Warehouse(
            name="Test Warehouse"
        )
        error = warehouse.validation.validate_unique_values()

        self.assertNotEqual(error, None)
    
    def test_should_not_return_error_given_warehouse_already_in_db(self):
        error = self.warehouse.validation.validate_unique_values()

        self.assertEqual(error, None)