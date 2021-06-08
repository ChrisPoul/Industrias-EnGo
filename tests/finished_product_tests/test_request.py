from . import FinishedProductTest
from EnGo.models.product import FinishedProduct


class TestAdd(FinishedProductTest):

    def test_should_add_finished_product_given_valid_finished_product(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            warehouse_id=1,
            quantity=1,
            unit="pz",
            cost=1
        )
        finished_product.request.add()

        self.assertIn(finished_product, self.db.session)

    def test_should_not_add_finished_product_given_invalid_finished_product(self):
        finished_product = FinishedProduct(
            product_id=self.product.id,
            warehouse_id=1,
            quantity="Invalid Quantity",
            unit="pz",
            cost=1
        )
        finished_product.request.add()

        self.assertNotIn(finished_product, self.db.session)


class TestUpdate(FinishedProductTest):

    def test_should_update_finished_product_given_valid_changes(self):
        self.finished_product.quantity = 2
        self.finished_product.request.update()
        self.db.session.rollback

        self.assertEqual(self.finished_product.quantity, 2)
    
    def test_should_not_update_finished_product_given_invalid_changes(self):
        self.finished_product.quantity = "Invalid Change"
        self.finished_product.request.update()
        self.db.session.rollback

        self.assertNotEqual(self.finished_product.quantity, "Invalid Change")
