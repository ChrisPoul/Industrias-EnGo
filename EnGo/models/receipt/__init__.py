from EnGo.models import db, MyModel
from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime,
    ForeignKey
)


class Receipt(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    sold_products = db.relationship(
        'SoldProduct',
        backref="receipt",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return self.folio

    def get(id):
        return Receipt.query.get(id)

    def get_all():
        return Receipt.query.all()

    @property
    def total(self):
        total = 0
        for sold_product in self.sold_products:
            total += sold_product.total

        return total

    @property
    def folio(self):
        id = str(self.id)
        folio = "REM "
        num_of_zeros = 5 - len(id)
        for _ in range(num_of_zeros):
            folio += "0"
        folio += id

        return folio

    @property
    def validation(self):
        from .validation import ReceiptValidation
        return ReceiptValidation(self)

    @property
    def products(self):
        return [sold_product.product for sold_product in self.sold_products]

    def add_product(self, product):
        from EnGo.models.product import SoldProduct
        sold_product = SoldProduct(
            receipt_id=self.id,
            product_id=product.id
        )
        sold_product.add()


def filter_receipts_by_date(receipts, date):
    filtered_receipts = []
    for receipt in receipts:
        if receipt.date.isocalendar() == date.isocalendar():
            filtered_receipts.append(receipt)

    return filtered_receipts
