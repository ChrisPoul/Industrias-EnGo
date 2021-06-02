from . import PostTest
from EnGo.models.post import Post


class TestAdd(PostTest):

    def test_should_add_post_given_valid_post(self):
        post = Post(
            title="Valid Title",
            description="Valid Description"
        )
        post.request.add()

        self.assertIn(post, self.db.session)
    
    def test_should_not_add_post_given_invalid_post(self):
        post = Post(
            title="Valid Title",
            description=""
        )
        post.request.add()

        self.assertNotIn(post, self.db.session)
    

class TestUpdate(PostTest):

    def test_should_update_post_given_valid_changes(self):
        self.post.description = "New Description"
        self.post.request.update()
        self.db.session.rollback()

        self.assertEqual(self.post.description, "New Description")
    
    def test_should_not_update_post_given_invalid_changes(self):
        self.post.description = ""
        self.post.request.update()
        self.db.session.rollback()

        self.assertNotEqual(self.post.description, "")