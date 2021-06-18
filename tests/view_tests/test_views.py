from . import ViewTest
from flask import url_for
from EnGo.models import permission
from EnGo.models.permission import Permission

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class TestUpdate(ViewTest):

    def setUp(self):
        ViewTest.setUp(self)
        self.create_test_users()

    def test_should_update_view_permissions_given_valid_permissions_input_and_LUHP(self):
        self.login_user(self.admin_user)
        permissions_input = dict(
            Admin=self.admin_permission.id
        )
        with self.client as client:
            client.post(
                url_for('view.update', id=self.view.id),
                data=permissions_input
            )
        self.db.session.rollback()

        self.assertIn(self.admin_permission, self.view.permissions)
