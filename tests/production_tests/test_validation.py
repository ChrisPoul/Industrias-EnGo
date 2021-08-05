from . import ProductionTest
from EnGo.models.production import Production


class TestValidate(ProductionTest):

    def test_should_not_return_error_given_valid_production(self):
        production = Production(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        error = production.validation.validate()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_invalid_production(self):
        production = Production(
            user_id=self.user.id,
            concept="",
            quantity=10
        )
        error = production.validation.validate()

        self.assertNotEqual(error, None)

    def test_should_return_error_given_invalid_user_id(self):
        production = Production(
            user_id=0,
            concept="Test Concept",
            quantity=10
        )
        error = production.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(ProductionTest):

    def test_should_not_return_error_given_no_empty_values(self):
        production = Production(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        error = production.validation.validate_empty_values()

        self.assertEqual(error, None)
    
    def test_should_return_error_given_empty_concept(self):
        production = Production(
            user_id=self.user.id,
            concept="",
            quantity=10
        )
        error = production.validation.validate_empty_values()

        self.assertNotEqual(error, None)
    
    def test_should_return_error_given_empty_quantity(self):
        production = Production(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=""
        )
        error = production.validation.validate_empty_values()

        self.assertNotEqual(error, None)


class TestValidateUserId(ProductionTest):

    def test_should_not_return_error_given_valid_user_id(self):
        production = Production(
            user_id=self.user.id
        )
        error = production.validation.validate_user_id()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_user_id(self):
        production = Production(
            user_id=0
        )
        error = production.validation.validate_user_id()

        self.assertNotEqual(error, None)
