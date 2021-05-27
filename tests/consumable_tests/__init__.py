from tests import Test
from EnGo.models.consumable import Consumable


class ConsumableTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.consumable = Consumable(
            consumable_name="Test Consumable"
        )
        self.consumable.add()
