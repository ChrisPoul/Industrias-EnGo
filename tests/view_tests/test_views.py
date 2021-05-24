from EnGo.models import permission
from . import ViewTest
from EnGo.models.permission import Permission


class ViewsTest(ViewTest):
    
    def setUp(self):
        ViewTest.setUp(self)
        self.admin_permission = Permission(
            permission_name="admin"
        )
        self.admin_permission.add()
    

