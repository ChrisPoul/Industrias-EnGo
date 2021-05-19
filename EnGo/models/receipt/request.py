from EnGo.models.product import Product


class ReceiptRequest:

    def __init__(self, receipt):
        self.receipt = receipt
    
    def edit(self, product=None):
        error = self.receipt.validation.validate()
        if not error:
            self.receipt.update()
            if product:
                self.add_product(product)

    def add_product(self, product_to_add):
        product = Product.search(product_to_add.code)
        if product:
            self.receipt.add_product(product)
        else:
            self.add_new_product(product_to_add)
    
    def add_new_product(self, product):
        error = product.request.add()
        if not error:
            self.receipt.add_product(product)
    