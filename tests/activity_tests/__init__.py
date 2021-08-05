from tests import Test
from EnGo.models.user import User
from EnGo.models.activity import Activity


class ActivityTest(Test):
    
    def setUp(self):
        Test.setUp(self)
        self.user = User(
            username="Test User",
            password="0000"
        )
        self.user.add()
        self.activity = Activity(
            user_id=self.user.id,
            title="Test Activity",
            description="Test Description"
        )
        self.activity.add()