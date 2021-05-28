from EnGo.models import consumable
from . import ConsumableTest
from EnGo.models.consumable import Consumable


class TestValidateEmptyValues(ConsumableTest):

    def test_should_not_return_error_given_valid_consumable(self):
        consumable = Consumable(
            consumable_name="Valid Name"
        )
        error = consumable.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empyt_value(self):
        consumable = Consumable(
            consumable_name=""
        )
        error = consumable.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateUniqueValues(ConsumableTest):

    def test_should_not_return_error_given_valid_consumable(self):
        consumable = Consumable(
            consumable_name="Valid Name"
        )
        error = consumable.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_repeated_value(self):
        consumable = Consumable(
            consumable_name="Test Consumable"
        )
        error = consumable.validation.validate()

        self.assertNotEqual(error, None)
    
    def test_should_not_return_error_given_consumable_already_in_db(self):
        error = self.consumable.validation.validate()

        self.assertEqual(error, None)
