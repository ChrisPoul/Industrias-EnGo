from EnGo.models import validate_empty_values


class PostValidation:

    def __init__(self, post):
        self.post = post
        self.error = None

    def validate(self):
        self.validate_empty_values()

        return self.error
    
    def validate_empty_values(self):
        post_attributes = [
            "title",
            "description"
        ]
        self.error = validate_empty_values(self.post, post_attributes)
        
        return self.error