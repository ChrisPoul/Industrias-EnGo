from EnGo.models.product import Product


class ReceiptRequest:

    def __init__(self, receipt):
        self.receipt = receipt
        self.error = None
    
    def update(self):
        error = self.receipt.validation.validate()
        if not error:
            self.receipt.update()
                
        return error
    