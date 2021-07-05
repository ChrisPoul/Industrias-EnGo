from . import UserTest
from EnGo.models.user import UserProduction


class ProductionTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.user_production = UserProduction(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        self.user_production.add()


class TestValidate(ProductionTest):

    def test_should_not_return_error_given_valid_user_production(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        error = user_production.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_invalid_user_production(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="",
            quantity=10
        )
        error = user_production.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(ProductionTest):

    def test_should_not_return_error_given_no_empty_values(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        error = user_production.validation.validate_empty_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_concept(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="",
            quantity=10
        )
        error = user_production.validation.validate_empty_values()

        self.assertNotEqual(error, None)
    
    def test_should_return_error_given_empty_quantity(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=""
        )
        error = user_production.validation.validate_empty_values()

        self.assertNotEqual(error, None)