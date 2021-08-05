from tests import Test
from EnGo.models.user import User
from EnGo.models.production import Production


class ProductionTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test User",
            password="0000"
        )
        self.user.add()
        self.production = Production(
            user_id=self.user.id,
            concept="Test Concept",
            quantity=10
        )
        self.production.add()