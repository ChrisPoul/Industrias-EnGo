from sqlalchemy import (
    Column, Integer, String,
)
from EnGo.models import db, MyModel

raw_material_attributes = [
    "material_name",
]


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

    @property
    def validation(self):
        from .validation import RawMaterialValidation
        return RawMaterialValidation(self)


from EnGo.models.warehouse import BoughtRawMaterial