from . import ProductTest
from EnGo.models.product import Product, FinishedProduct, SoldProduct


class TestAdd(ProductTest):

    def test_should_add_product(self):
        product = Product(
            warehouse_id=1,
            code="Some Code",
            description="Optional description",
            price=10
        )
        product.add()

        self.assertIn(product, self.db.session)


class TestUpdate(ProductTest):
    
    def test_should_update_product(self):
        self.product.code = "New Code"
        self.product.update()
        self.db.session.rollback()

        self.assertEqual(self.product.code, "New Code")


class TestDelete(ProductTest):

    def test_should_delete_product(self):
        self.product.delete()

        self.assertNotIn(self.product, self.db.session)


class TestGet(ProductTest):

    def test_should_return_product_given_valid_id(self):
        product = Product.get(1)

        self.assertEqual(product, self.product)
    
    def test_should_return_none_given_invalid_id(self):
        product = Product.get(2)

        self.assertEqual(product, None)


class TestGetAll(ProductTest):

    def test_should_return_a_list_of_all_products(self):
        products = Product.get_all()

        self.assertEqual(products, [self.product])


class TestSearch(ProductTest):

    def test_should_return_product_given_valid_code(self):
        product = Product.search('Test Code')

        self.assertEqual(product, self.product)


class TestInventory(ProductTest):

    def setUp(self):
        ProductTest.setUp(self)
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity=10,
            unit="pz"
        )
        finished_product.add()
        sold_product = SoldProduct(
            receipt_id=1,
            product_id=self.product.id,
            unit="pz",
            quantity=5,
            price=self.product.price
        )
        sold_product.add()
        finished_product = FinishedProduct(
            product_id=self.product.id,
            quantity=10,
            unit="kg"
        )
        finished_product.add()
        sold_product = SoldProduct(
            receipt_id=1,
            product_id=self.product.id,
            unit="kg",
            quantity=5,
            price=self.product.price
        )
        sold_product.add()

    def test_should_return_dictionary_with_each_units_inventory(self):
        inventory = self.product.inventory

        self.assertEqual(inventory["pz"], 5)
        self.assertEqual(inventory["kg"], 5)