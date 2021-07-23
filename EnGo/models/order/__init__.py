from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, Date, Text
)
from EnGo.models import db, MyModel


class Order(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Pendiente")
    due_date = Column(Date, nullable=False)
    assignment_date = Column(Date, nullable=False, default=datetime.today)

    @property
    def validation(self):
        from .validation import OrderValidation
        return OrderValidation(self)

    @property
    def request(self):
        from .request import OrderRequest
        return OrderRequest(self)
