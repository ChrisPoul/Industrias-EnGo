from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, Text, Date
)
from EnGo.models import db, MyModel


class Activity(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=False, default=datetime.today)

    @property
    def validation(self):
        from .validation import ActivityValidation
        return ActivityValidation(self)
