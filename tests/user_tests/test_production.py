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
    

class TestAddRequest(ProductionTest):

    def test_should_add_user_production_given_valid_user_production(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        user_production.request.add()

        self.assertIn(user_production, self.db.session)
    
    def test_should_not_add_user_production_given_invalid_user_production(self):
        user_production = UserProduction(
            user_id=self.user.id,
            concept="",
            quantity=10
        )
        user_production.request.add()

        self.assertNotIn(user_production, self.db.session)


class TestUpdateRequest(ProductionTest):

    def test_should_update_user_production_given_valid_changes(self):
        self.user_production.concept = "New Concept"
        self.user_production.request.update()
        self.db.session.rollback()

        self.assertEqual(self.user_production.concept, "New Concept")
    
    def test_should_not_update_user_production_given_invalid_changes(self):
        self.user_production.concept = ""
        self.user_production.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.user_production.concept, "")

