from . import ConsumableTest
from EnGo.models.consumable import Consumable


class TestAdd(ConsumableTest):

    def test_should_add_consumable_given_valid_consumable(self):
        consumable = Consumable(
            consumable_name="Valid Name"
        )
        consumable.request.add()

        self.assertIn(consumable, self.db.session)
    
    def test_should_not_add_consumable_given_invalid_consumable(self):
        consumable = Consumable(
            consumable_name=""
        )
        consumable.request.add()

        self.assertNotIn(consumable, self.db.session)