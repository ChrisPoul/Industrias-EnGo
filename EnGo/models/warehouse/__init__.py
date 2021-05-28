from tests import warehouse_tests
from sqlalchemy import (
    Column, Integer, String
)
from EnGo.models import db, MyModel
from EnGo.models.raw_material import BoughtRawMaterial

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
    def validation(self):
        from .validation import WarehouseValidation
        return WarehouseValidation(self)

    @property
    def products(self):
        return [finished_product.product for finished_product in self.finished_products]

    def add_product(self, product):
        from EnGo.models.product import FinishedProduct
        finished_product = FinishedProduct(
            product_id=product.id,
            warehouse_id=self.id
        )
        finished_product.add()
    
    @property
    def consumables(self):
        return [bought_consumable.consumable for bought_consumable in self.bought_consumables]

    def add_consumable(self, consumable):
        from EnGo.models.consumable import BoughtConsumable
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
