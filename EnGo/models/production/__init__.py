from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime
)
from EnGo.models import db, MyModel


class Production(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    concept = Column(String(200), nullable=False, unique=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    quantity = Column(Integer, nullable=False)

    @property
    def validation(self):
        from .validation import ProductionValidation
        return ProductionValidation(self)