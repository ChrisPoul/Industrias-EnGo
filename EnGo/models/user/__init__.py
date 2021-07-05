from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime, Text
)
from EnGo.models import db, MyModel
from EnGo.models.view import View


class User(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    salary = Column(Integer, nullable=False, default=0)
    contract = db.relationship(
        "Contract",
        backref="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    observations = db.relationship(
        'UserObservation',
        backref="user",
        cascade="all, delete-orphan"
    )
    activities = db.relationship(
        'UserActivity',
        backref="user",
        cascade="all, delete-orphan"
    )
    user_permissions = db.relationship(
        'UserPermission',
        backref="user",
        cascade="all, delete-orphan"
    )
    production = db.relationship(
        'UserProduction',
        backref="user",
        cascade="all, delete-orphan"
    )

    def get(id):
        return User.query.get(id)

    def get_all():
        return User.query.all()

    def search(username):
        return User.query.filter_by(username=username).first()

    @property
    def permissions(self):
        return [user_permission.permission for user_permission in self.user_permissions]

    @property
    def validation(self):
        from .validation import UserValidation
        return UserValidation(self)

    @property
    def request(self):
        from .request import UserRequest
        return UserRequest(self)

    def has_view_permissions(self, view_name):
        view = View.search(view_name)
        if self.is_dev() or not view:
            return True
        if self.is_admin() and not view.requires_dev():
            return True
        for permission in self.permissions:
            if permission in set(view.permissions):
                return True
        
        return False

    def is_admin(self):
        return self.has_permissions(["Admin", "Dev"])

    def is_dev(self):
        return self.has_permissions(["Dev"])

    def has_permissions(self, permission_names):
        for permission in self.permissions:
            if permission.permission_name in set(permission_names):
                return True
        
        return False

    def add_permission(self, permission):
        user_permission = UserPermission(
            user_id=self.id,
            permission_id=permission.id
        )
        user_permission.add()
    
    def add_permissions(self, permissions):
        for permission in permissions:
            self.add_permission(permission)
    
    def remove_permissions(self):
        for user_permission in self.user_permissions:
            user_permission.delete()

    def update_permissions(self, permissions):
        self.remove_permissions()
        self.add_permissions(permissions)

    def get_week_activities(self, date=datetime.today):
        week_activities = filter_activities_by_week(date, self.activities)
        weekday_activities = {}
        for weekday_num in range(7):
            weekday_activities[weekday_num] = []
        for activity in week_activities:
            week_day = activity.due_date.weekday()
            weekday_activities[week_day].append(activity)

        return weekday_activities
    
    def get_day_activities(self, date):
        week_activities = self.get_week_activities(date)
        day = date.weekday()
        
        return week_activities[day]

def filter_activities_by_week(date, events):
    week_events = []
    for event in events:
        date_year, date_week, _ = date.isocalendar()
        due_year, due_week, _ = event.due_date.isocalendar()
        if due_year == date_year and due_week == date_week:
            week_events.append(event)
    
    return week_events
        

class UserObservation(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)


class UserPermission(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    permission_id = Column(Integer, ForeignKey('permission.id'), nullable=False)


class UserActivity(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    assignment_date = Column(DateTime, nullable=False, default=datetime.now)
    due_date = Column(DateTime, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    @property
    def validation(self):
        from .validation import UserActivityValidation
        return UserActivityValidation(self)

    @property
    def request(self):
        from .request import UserActivityRequest
        return UserActivityRequest(self)


class UserProduction(db.Model, MyModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    concept = Column(String(200), nullable=False, unique=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    quantity = Column(Integer, nullable=False)

    @property
    def request(self):
        from .request import UserProductionRequest
        return UserProductionRequest(self)

    @property
    def validation(self):
        from .validation import UserProductionValidation
        return UserProductionValidation(self)


from .contract import Contract