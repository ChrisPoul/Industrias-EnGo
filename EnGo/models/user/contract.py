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
    def daily_salary(self):
        return self.user.salary / 30

    @property
    def duration(self):
        if not self.end:
            return None
        duration = self.end - self.start

        return duration.days

    @property
    def seniority(self):
        seniority = datetime.today() - self.start

        return seniority.days

    @property
    def vacation_days(self):
        seniority_years = get_elapsed_years(self.start, datetime.today())
        if seniority_years == 0:
            return 0
        vacation_days = 6
        for year in range(2, seniority_years + 1):
            if year <= 4:
                vacation_days += 2
        for year in range(5, seniority_years, 5):
            vacation_days += 2

        return vacation_days
    
    @property
    def vacation_bonus(self):
       return self.vacation_days * self.daily_salary * 0.25


def get_elapsed_years(start_date, end_date):
    elapsed_days = (end_date - start_date).days
    elapsed_years = 0
    for year in range(start_date.year, end_date.year):
        if year % 4 == 0:
            elapsed_days -= 366
        else:
            elapsed_days -= 365
        if elapsed_days >= 0:
            elapsed_years += 1


    return elapsed_years
