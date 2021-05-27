from . import ConsumableTest
from EnGo.models.consumable import Consumable


class TestAdd(ConsumableTest):

    def test_should_add_consumable(self):
        consumable = Consumable(
            consumable_name="Some Consumable"
        )
        consumable.add()

        self.assertIn(consumable, self.db.session)


class TestUpdate(ConsumableTest):

    def test_should_update_consumable(self):
        self.consumable.consumable_name = "New Name"
        self.consumable.update()
        self.db.session.rollback()

        self.assertEqual(self.consumable.consumable_name, "New Name")


class TestDelete(ConsumableTest):

    def test_should_delete_consumable(self):
        self.consumable.delete()

        self.assertNotIn(self.consumable, self.db.session)