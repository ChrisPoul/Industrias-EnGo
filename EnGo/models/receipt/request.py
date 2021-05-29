from EnGo.models.product import Product


class ReceiptRequest:

    def __init__(self, receipt):
        self.receipt = receipt
        self.error = None
    
    def edit(self):
        error = self.receipt.validation.validate()
        if not error:
            self.receipt.update_product_inventories()
            self.receipt.update()
                
        return error

    def add_product(self, product_to_add):
        product = Product.search(product_to_add.code)
        if product and product not in set(self.receipt.products):
            self.receipt.add_product(product)
        else:
            self.add_new_product(product_to_add)

        return self.error
    
    def add_new_product(self, product):
        self.error = product.request.add()
        if not self.error:
            self.receipt.add_product(product)
    