from flask_testing import TestCase
from EnGo import create_app
from EnGo.models import db
from EnGo.models.permission import Permission
from EnGo.models.user import User


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

    def request_context(self, url, data={}):
        with self.client:
            with self.app.test_request_context(url, data=data) as request_context:
                return request_context

    def create_test_users(self):
        self.admin_permission = Permission(
            permission_name="Admin",
        )
        self.admin_permission.add()
        self.admin_user = User(
            username="Admin User",
            password="0000"
        )
        self.admin_user.add()
        self.admin_user.add_permission(self.admin_permission)
        accounting_permission = Permission(
            permission_name="Contaduría"
        )
        accounting_permission.add()
        self.accounting_user = User(
            username="Accounting User",
            password="0000"
        )
        self.accounting_user.add()
        self.accounting_user.add_permission(accounting_permission)
        self.normal_user = User(
            username="Normal User",
            password="0000"
        )
        self.normal_user.add()

    def login_user(self, user):
        with self.client.session_transaction() as session:
            session["user_id"] = user.id
