from . import Test
from flask import url_for
from EnGo.models.permission import Permission
from EnGo.models.user import User, UserPermission
from EnGo.models.product import Product


class ProductViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.product = Product(
            code="Test Code",
            description="Optional description",
            price=10
        )
        self.product.add()
        permission = Permission(
            permission_name="contaduría"
        )
        permission.add()
        accounting_user = User(
            username="Accounting User",
            password="0000"
        )
        accounting_user.add()
        user_permission = UserPermission(
            user_id=accounting_user.id,
            permission_id=permission.id
        )
        user_permission.add()
        with self.client.session_transaction() as session:
            session["user_id"] = accounting_user.id
        self.normal_user = User(
            username="Normal User",
            password="0000"
        )
        self.normal_user.add()


class TestAddView(ProductViewTest):

    def test_should_add_product_given_valid_product_data_and_loged_in_user_has_permission(self):
        product_data = dict(
            code="Valid Code",
            description="Some description",
            price="10"
        )
        with self.client as client:
            client.post(
                url_for("product.add"),
                data=product_data
            )

        self.assertEqual(len(Product.get_all()), 2)

    def test_should_not_add_product_given_invalid_product_data_and_loged_in_user_has_permission(self):
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

    def test_should_redirect_given_loged_in_user_does_not_have_permission(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for("product.add")
        )
        
        self.assertStatus(response, 302)


class TestUpdateView(ProductViewTest):

    def test_should_update_product_given_valid_product_data_and_loged_in_user_has_permission(self):
        product_data = dict(
            code="New Code",
            description="",
            price="20"
        )
        with self.client as client:
            client.post(
                url_for("product.update", id=self.product.id),
                data=product_data
            )
        self.db.session.rollback()
        
        self.assertEqual(self.product.code, "New Code")

    def test_should_redirect_given_loged_in_user_does_not_have_permission(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for("product.update", id=1)
        )

        self.assertStatus(response, 302)


class TestDeleteView(ProductViewTest):

    def test_should_delete_product_given_loged_in_user_has_permission(self):
        with self.client as client:
            client.get(
                url_for("product.delete", id=self.product.id)
            )

        self.assertNotIn(self.product, self.db.session)

    def test_should_redirect_given_loged_in_user_does_not_have_permission(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for("product.delete", id=1)
        )
        
        self.assertStatus(response, 302)


class TestProductsView(ProductViewTest):

    def test_should_return_valid_response_given_loged_in_user_has_permission(self):
        with self.client as client:
            response = client.get(
                url_for("product.products")
            )

        self.assert200(response)

    def test_should_redirect_given_loged_in_user_does_not_have_permission(self):
        with self.client.session_transaction() as session:
            session["user_id"] = self.normal_user.id
        response = self.client.get(
            url_for("product.products")
        )
        
        self.assertStatus(response, 302)
