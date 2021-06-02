from tests import Test
from EnGo.models.post import Post


class PostTest(Test):

    def setUp(self):
        Test.setUp(self)
        self.post = Post(
            title="Title",
            description="Description"
        )
        self.post.add()
