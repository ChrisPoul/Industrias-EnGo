

class PostRequest:

    def __init__(self, post):
        self.post = post
    
    def add(self):
        error = self.post.validation.validate()
        if not error:
            self.post.add()

        return error
    
    def update(self):
        error = self.post.validation.validate()
        if not error:
            self.post.update()
        
        return error
