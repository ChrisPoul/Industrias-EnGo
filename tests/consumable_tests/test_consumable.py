from EnGo.models.raw_material import RawMaterial
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


class TestGet(ConsumableTest):

    def test_should_return_consumable_given_valid_id(self):
        consumable = Consumable.get(self.consumable.id)

        self.assertEqual(consumable, self.consumable)


class TestGetAll(ConsumableTest):

    def test_should_return_all_consumables(self):
        consumables = Consumable.get_all()

        self.assertEqual(consumables, [self.consumable])


class TestSearch(ConsumableTest):

    def test_should_return_consumable_given_valid_search_term(self):
        consumable = Consumable.search(self.consumable.consumable_name)

        self.assertEqual(consumable, self.consumable)

