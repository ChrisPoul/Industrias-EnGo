class ObjectRequest:

    def __init__(self, obj):
        self.obj = obj
    
    def add(self):
        error = self.obj.validation.validate()
        if not error:
            self.obj.add()
        
        return error

    def update(self):
        error = self.obj.validation.validate()
        if not error:
            self.obj.update()
        
        return error