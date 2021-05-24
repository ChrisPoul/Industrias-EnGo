from . import ViewTest
from flask import url_for
from EnGo.models import permission
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ViewsTest(ViewTest):
    
    def setUp(self):
        ViewTest.setUp(self)
        self.create_test_users()


class TestUpdate(ViewsTest):

    def test_should_update_view_permissions_given_LUHP(self):
        self.login_user(self.admin_user)
        permissions_data = dict(
            admin=self.admin_permission.id
        )
        with self.client as client:
            client.post(
                url_for('view.update', id=self.view.id),
                data=permissions_data
            )
        self.db.session.rollback()

        self.assertIn(self.admin_permission, self.view.permissions)
