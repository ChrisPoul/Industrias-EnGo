from tests import Test
from EnGo.models.view import View


class ViewTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.view = View(
            view_name="Test View"
        )
        self.view.add()