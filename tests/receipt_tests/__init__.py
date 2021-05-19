from tests import Test
from datetime import datetime
from EnGo.models.receipt import Receipt


class ReceiptTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.receipt = Receipt()
        self.receipt.add()