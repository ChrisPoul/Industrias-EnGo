from . import PostTest
from flask import url_for
from EnGo.models.post import Post

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class PostRequestTest(PostTest):

    def setUp(self):
        PostTest.setUp(self)
        self.create_test_users()

    
class TestAddView(PostRequestTest):

    def test_should_add_post_given_valid_post_data_and_LUHP(self):
        self.login_user(self.admin_user)
        post_data = dict(
            title="Valid Title",
            description="Valid Description"
        )
        with self.client as client:
            client.post(
                url_for("post.add"),
                data=post_data
            )
        
        self.assertTrue(Post.search("Valid Title"))
    
    def test_should_not_add_post_given_invalid_post_data_and_LUHP(self):
        self.login_user(self.admin_user)
        post_data = dict(
            title="",
            description="Valid Description"
        )
        with self.client as client:
            client.post(
                url_for('post.add'),
                data=post_data
            )
        
        self.assertFalse(Post.search(""))
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('post.add')
            )
        
        self.assertStatus(response, 302)


class TestUpdateView(PostRequestTest):

    def test_should_update_post_given_valid_post_changes_and_LUHP(self):
        self.login_user(self.admin_user)
        post_data = dict(
            title="New Title",
            description="Test Description"
        )
        with self.client as client:
            client.post(
                url_for('post.update', id=self.post.id),
                data=post_data
            )
        self.db.session.rollback()
        
        self.assertEqual(self.post.title, "New Title")

    def test_should_not_update_post_given_invalid_changes_and_LUHP(self):
        self.login_user(self.admin_user)
        post_data = dict(
            title="",
            description="Test Description"
        )
        with self.client as client:
            client.post(
                url_for('post.update', id=self.post.id),
                data=post_data
            )
        self.db.session.rollback()
        
        self.assertNotEqual(self.post.title, "")
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('post.update', id=self.post.id)
            )
        
        self.assertStatus(response, 302)


class TestDeleteView(PostRequestTest):

    def test_should_delete_post_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            client.get(
                url_for('post.delete', id=self.post.id)
            )
        
        self.assertNotIn(self.post, self.db.session)
    
    def test_should_not_delete_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            client.get(
                url_for('post.delete', id=self.post.id)
            )
        
        self.assertIn(self.post, self.db.session)