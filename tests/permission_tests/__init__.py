from tests import Test
from EnGo.models.permission import Permission


class PermissionTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.admin_permission = Permission(
            permission_name="admin",
            description="Gives acces to all aspects of the system"
        )
        self.admin_permission.add()