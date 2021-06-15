from datetime import datetime
from EnGo.models import db, MyModel
from sqlalchemy import (
    Column, String, Integer,
    DateTime, ForeignKey
)


class Contract(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    type = Column(String(100), nullable=True)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)

    @property
    def duration(self):
        return 1

