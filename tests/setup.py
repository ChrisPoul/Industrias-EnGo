from flask_testing import TestCase
from EnGo import create_app
from EnGo.models import db


class Test(TestCase):

    def create_app(self):
        test_config = {
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "TESTING": True
        }
        app = create_app(test_config)

        return app

    def setUp(self):
        self.client = self.app.test_client()
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def request_context(self, url, data):
        with self.client:
            with self.app.test_request_context(url, data=data) as request_context:
                return request_context