from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime
)
from EnGo.models import db, MyModel
from EnGo.models.raw_material import RawMaterial

warehouse_attributes = [
    'address'
]

class Warehouse(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False, unique=True)
    finished_products = db.relationship(
        'FinishedProduct',
        backref="warehouse",
        cascade="all, delete-orphan"
    )
    bought_consumables = db.relationship(
        'BoughtConsumable',
        backref="warehouse",
        cascade="all, delete-orphan"
    )
    bought_raw_materials = db.relationship(
        'BoughtRawMaterial',
        backref="warehouse",
        cascade="all, delete-orphan"
    )

    def get(id):
        return Warehouse.query.get(id)

    def get_all():
        return Warehouse.query.all()
    
    def search(search_term):
        return Warehouse.query.filter_by(address=search_term).first()
    
    @property
    def request(self):
        from .request import WarehouseRequest
        return WarehouseRequest(self)
    
    @property
    def validation(self):
        from .validation import WarehouseValidation
        return WarehouseValidation(self)

    @property
    def products(self):
        return [finished_product.product for finished_product in self.finished_products]

    def add_product(self, product):
        finished_product = FinishedProduct(
            product_id=product.id,
            warehouse_id=self.id
        )
        finished_product.add()
    
    @property
    def consumables(self):
        return [bought_consumable.consumable for bought_consumable in self.bought_consumables]

    def add_consumable(self, consumable):
        bought_consumable = BoughtConsumable(
            consumable_id=consumable.id,
            warehouse_id=self.id,
            price=consumable.price
        )
        bought_consumable.add()
    
    @property
    def raw_materials(self):
        return [bought_raw_material.raw_material for bought_raw_material in self.bought_raw_materials]
    
    def add_raw_material(self, raw_material):
        bought_raw_material = BoughtRawMaterial(
            raw_material_id=raw_material.id,
            warehouse_id=self.id,
            price=raw_material.price
        )
        bought_raw_material.add()


class BoughtRawMaterial(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    raw_material_id = Column(Integer, ForeignKey('raw_material.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    price = Column(Integer, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def get(id):
        return BoughtRawMaterial.query.get(id)


class FinishedProduct(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    inventory = Column(Integer, nullable=False, default=0)
    unit = Column(String(10), nullable=False, default="pz")
    cost = Column(Integer, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def get(id):
        return FinishedProduct.query.get(id)


class BoughtConsumable(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    consumable_id = Column(Integer, ForeignKey('consumable.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False, default=0)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def get(id):
        return BoughtConsumable.query.get(id)


from EnGo.models.consumable import Consumable