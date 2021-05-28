from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.sql.schema import ForeignKey
from EnGo.models import db, MyModel


class RawMaterial(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    material_name = Column(String(200), nullable=False, unique=True)
    price = Column(Integer, nullable=False, default=0)
    bought_raw_materials = db.relationship(
        'BoughtRawMaterial',
        backref="raw_material",
        cascade="all, delete-orphan"
    )

    def get(id):
        return RawMaterial.query.get(id)
    
    def get_all():
        return RawMaterial.query.all()
    
    def search(search_term):
        return RawMaterial.query.filter_by(material_name=search_term).first()


class BoughtRawMaterial(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    raw_material_id = Column(Integer, ForeignKey('raw_material.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    price = Column(Integer, nullable=False, default=0)

    def get(id):
        return BoughtRawMaterial.query.get(id)

