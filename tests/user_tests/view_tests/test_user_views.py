from . import UserViewTest
from flask import url_for

### LOGED IN USER (LU) ###
### LOGED IN USER HAS PERMISSION (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class TestUsersView(UserViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            response = client.get(
                url_for('user.users')
            )
        
        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('user.users')
            )

        self.assertStatus(response, 302)

    def test_should_redirect_given_valid_search_term_and_LUHP(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Test User"
        )
        with self.client as client:
            response = client.post(
                url_for('user.users'),
                data=search_data
            )
        
        self.assertStatus(response, 302)

    def test_should_not_redirect_given_invalid_search_term_and_LUHP(self):
        self.login_user(self.admin_user)
        search_data = dict(
            search_term="Invalid term"
        )
        with self.client as client:
            response = client.post(
                url_for('user.users'),
                data=search_data
            )
        
        self.assert200(response)
    

class TestUpdateView(UserViewTest):

    def test_should_update_user_given_valid_user_data_and_LUHP(self):
        self.login_user(self.admin_user)
        user_data = dict(
            username="New Username",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.update', id=self.user.id),
                data=user_data
            )
        self.db.session.rollback()

        self.assertEqual(self.user.username, "New Username")

    def test_should_not_update_user_given_invalid_user_data_and_LUHP(self):
        self.login_user(self.admin_user)
        user_data = dict(
            username="",
            password="0000",
            salary=1000
        )
        with self.client as client:
            client.post(
                url_for('user.update', id=self.user.id),
                data=user_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.user.username, "")

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('user.update', id=self.user.id)
            )

        self.assertStatus(response, 302)


class TestDeleteView(UserViewTest):

    def test_should_delete_user_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            client.get(
                url_for('user.delete', id=self.normal_user.id)
            )

        self.assertNotIn(self.normal_user, self.db.session)


class TestProfileView(UserViewTest):

    def test_should_grant_access_given_LUHP(self):
        self.login_user(self.dev_user)
        with self.client as client:
           response = client.get(
                url_for('user.profile', id=self.normal_user.id)
            )

        self.assert200(response)

    def test_should_grant_access_given_profile_belongs_to_LU(self):
        self.login_user(self.normal_user)
        with self.client as client:
           response = client.get(
                url_for('user.profile', id=self.normal_user.id)
            )

        self.assert200(response)
