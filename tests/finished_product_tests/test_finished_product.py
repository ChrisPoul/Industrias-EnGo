from . import FinishedProductTest
from EnGo.models.product import FinishedProduct


class TestAdd(FinishedProductTest):

    def test_should_add_finished_product(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            warehouse_id=1,
            quantity=1,
            unit="pz",
            cost=1
        )
        finished_product.add()

        self.assertIn(finished_product, self.db.session)
    

class TestUpdate(FinishedProductTest):

    def test_should_update_finished_product(self):
        self.finished_product.quantity = 2
        self.finished_product.update()
        self.db.session.rollback()

        self.assertEqual(self.finished_product.quantity, 2)


class TestDelete(FinishedProductTest):

    def test_should_delete_finished_product(self):
        self.finished_product.delete()

        self.assertNotIn(self.finished_product, self.db.session)

