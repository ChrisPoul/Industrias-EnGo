from . import ProductTest
from flask import url_for
from EnGo.models.permission import Permission
from EnGo.models.user import User
from EnGo.models.product import Product

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ProductViewTest(ProductTest):

    def setUp(self):
        ProductTest.setUp(self)
        self.create_test_users()


class TestProductsView(ProductViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            response = client.get(
                url_for("product.products")
            )

        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        response = self.client.get(
            url_for("product.products")
        )
        
        self.assertStatus(response, 302)

    def test_should_redirect_given_valid_search_term_and_LUHP(self):
        self.login_user(self.accounting_user)
        search_data = dict(
            search_term="Test Code"
        )
        with self.client as client:
            response = client.post(
                url_for('product.products'),
                data=search_data
            )
        
        self.assertStatus(response, 302)

    def test_should_not_redirect_given_invalid_search_term_and_LUHP(self):
        self.login_user(self.accounting_user)
        search_data = dict(
            search_term="Invalid term"
        )
        with self.client as client:
            response = client.post(
                url_for('product.products'),
                data=search_data
            )
        
        self.assert200(response)


class TestAddView(ProductViewTest):

    def test_should_add_product_given_valid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        product_data = dict(
            code="Valid Code",
            description="Some description",
            price=10
        )
        with self.client as client:
            client.post(
                url_for("product.add"),
                data=product_data
            )

        self.assertEqual(len(Product.get_all()), 2)

    def test_should_not_add_product_given_invalid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        product_data = dict(
            code="",
            description="Some description",
            price="invalid price"
        )
        with self.client as client:
            client.post(
                url_for("product.add"),
                data=product_data
            )

        self.assertEqual(len(Product.get_all()), 1)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        response = self.client.get(
            url_for("product.add")
        )
        
        self.assertStatus(response, 302)


class TestUpdateView(ProductViewTest):

    def test_should_update_product_given_valid_product_data_and_LUHP(self):
        self.login_user(self.accounting_user)
        product_data = dict(
            code="New Code",
            description="",
            price=20
        )
        with self.client as client:
            client.post(
                url_for("product.update", id=self.product.id),
                data=product_data
            )
        self.db.session.rollback()
        
        self.assertEqual(self.product.code, "New Code")

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        response = self.client.get(
            url_for("product.update", id=1)
        )

        self.assertStatus(response, 302)


class TestDeleteView(ProductViewTest):

    def test_should_delete_product_given_LUHP(self):
        self.login_user(self.accounting_user)
        with self.client as client:
            client.get(
                url_for("product.delete", id=self.product.id)
            )

        self.assertNotIn(self.product, self.db.session)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        response = self.client.get(
            url_for("product.delete", id=1)
        )
        
        self.assertStatus(response, 302)
