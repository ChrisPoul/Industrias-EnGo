from EnGo.models import db, MyModel
from datetime import datetime
from sqlalchemy import (
    Column, Integer, DateTime
)


class Receipt(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.now)

    def get(id):
        return Receipt.query.get(id)

    def get_all():
        return Receipt.query.all()
