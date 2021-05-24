

class ReceiptValidation:

    def __init__(self, receipt):
        self.receipt = receipt
        self.error = None

    def validate(self):
        self.validate_customer()
        if not self.error:
            self.validate_products()
        if not self.error:
            self.validate_sold_products()

        return self.error

    def validate_customer(self):
        self.error = self.receipt.customer.validation.validate()

        return self.error

    def validate_products(self):
        for product in self.receipt.products:
            self.error = product.validation.validate()
            if self.error:
                break

        return self.error

    def validate_sold_products(self):
        return self.error