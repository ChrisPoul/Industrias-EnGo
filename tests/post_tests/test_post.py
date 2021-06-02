from . import PostTest
from EnGo.models.post import Post


class TestAdd(PostTest):

    def test_should_add_post(self):
        post = Post(
            title="Title",
            description="Description"
        )
        post.add()

        self.assertIn(post, self.db.session)


class TestUpdate(PostTest):

    def test_should_update_post(self):
        self.post.title = "New Title"
        self.post.update()
        self.db.session.rollback()

        self.assertEqual(self.post.title, "New Title")


class TestDelete(PostTest):

    def test_should_delete_post(self):
        self.post.delete()

        self.assertNotIn(self.post, self.db.session)


class TestGet(PostTest):

    def test_should_return_post_given_valid_id(self):
        post = Post.get(self.post.id)

        self.assertEqual(post, self.post)


class TestGetAll(PostTest):

    def test_should_return_all_posts(self):
        posts = Post.get_all()

        self.assertEqual(posts, [self.post])


class TestSearch(PostTest):

    def test_should_return_post_given_search_term(self):
        search_result = Post.search("Title")

        self.assertEqual(search_result, self.post)

