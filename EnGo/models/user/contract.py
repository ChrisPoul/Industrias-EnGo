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
        if not self.end:
            return None

        return get_elapsed_time(self.start, self.end, "days")

    @property
    def seniority(self):
        
        return get_elapsed_time(self.start, datetime.today(), "days")

    @property
    def vacation_days(self):
        seniority_years = get_elapsed_time(self.start, datetime.today(), "years")
        if seniority_years == 0:
            return 0
        vacation_days = 6
        for year in range(1, seniority_years + 1):
            if year > 1 and year <= 4:
                vacation_days += 2
        for year in range(5, seniority_years, 4):
            vacation_days += 2

        return vacation_days


def get_elapsed_time(start_date, end_date, time_period="days"):
    if time_period == "days":
        elapsed_time = (end_date - start_date).days
    elif time_period == "years":
        elapsed_time = end_date.year - start_date.year
    elif time_period == "months":
        elapsed_years = end_date.year - start_date.year
        elapsed_time = end_date.month - start_date.month + (elapsed_years * 12)
    else:
        raise ValueError("Invalid Time Period")

    return elapsed_time
