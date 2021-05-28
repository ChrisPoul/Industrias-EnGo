


class ConsumableRequest:

    def __init__(self, consumable):
        self.consumable = consumable
        self.error = None
    
    def add(self):
        self.error = self.consumable.validation.validate()
        if not self.error:
            self.consumable.add()
        
        return self.error
