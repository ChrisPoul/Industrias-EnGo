from . import PostTest
from EnGo.models.post import Post


class TestValidation(PostTest):
     
    def test_should_not_return_error_given_valid_post(self):
        post = Post(
            title="Valid Post",
            description="Valid Description"
        )
        error = post.validation.validate()

        self.assertEqual(error, None)

    def test_should_return_error_given_invalid_post(self):
        post = Post(
            title="",
            description="Test Description"
        )
        error = post.validation.validate()

        self.assertNotEqual(error, None)


class TestValidateEmptyValues(PostTest):

    def test_should_not_return_error_given_no_empty_values(self):
        post = Post(
            title="Valid Title",
            description="Valid Description"
        )
        error = post.validation.validate_empty_values()

        self.assertEqual(error, None)
         
    def test_should_return_error_given_empty_values(self):
        post = Post(
            title="",
            description="Valid Description"
        )
        error = post.validation.validate_empty_values()

        self.assertNotEqual(error, None)

