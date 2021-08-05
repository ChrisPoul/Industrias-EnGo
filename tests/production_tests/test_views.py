from . import ProductionTest
from flask import url_for

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ProductionViewTest(ProductionTest):

    def setUp(self):
        ProductionTest.setUp(self)
        self.production.delete()
        self.create_test_users()


class TestRegisterView(ProductionViewTest):

    def test_should_register_production_given_valid_production_input_and_LUHP(self):
        self.login_user(self.dev_user)
        production_input = dict(
            concept="New Production",
            quantity=10,
            user_id=self.user.id
        )
        with self.client as client:
            client.post(
                url_for('production.register'),
                data=production_input
            )

        self.assertEqual(len(self.user.production), 1)
    
    def test_should_not_register_production_given_invalid_production_input_and_LUHP(self):
        self.login_user(self.dev_user)
        production_input = dict(
            concept="",
            quantity=10,
            user_id=self.user.id
        )
        with self.client as client:
            client.post(
                url_for('production.register'),
                data=production_input
            )
        
        self.assertEqual(len(self.user.production), 0)
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('production.register')
            )
        
        self.assertStatus(response, 302)


class TestProductionView(ProductionViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.dev_user)
        with self.client as client:
            response = client.get(
                url_for('production.production')
            )
        
        self.assert200(response)
