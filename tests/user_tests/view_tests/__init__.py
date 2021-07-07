from tests.user_tests import UserTest
from werkzeug.security import generate_password_hash

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class UserViewTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.user.password = generate_password_hash(self.user.password)
        self.user.update()
        self.create_test_users()
