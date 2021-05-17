from . import Test
from EnGo.models.product import Product


class ProductTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()


class TestAdd(Test):

    def test_should_add_product(self):
        product = Product(
            code="Test Code",
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