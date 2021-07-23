from EnGo.models.calendar import MyCalendar


class UserSchedule:

    def __init__(self, user):
        self.user = user

    def get_weekday_activities(self, date):
        weekday_activities = {}
        weekday_dates = MyCalendar.get_weekday_dates(date)
        for weekday in weekday_dates:
            day_activities = self.get_day_activities(weekday_dates[weekday])
            weekday_activities[weekday] = day_activities

        return weekday_activities
    
    def get_week_activities(self, date):
        week_activities = []
        weekday_dates = MyCalendar.get_weekday_dates(date)
        for day in weekday_dates.values():
            day_activities = self.get_day_activities(day)
            week_activities += day_activities

        return week_activities

    def get_finished_week_activities(self, date):
        week_activities = self.get_week_activities(date)

        return [activity for activity in week_activities if activity.status == "Completada"]

    def get_pending_week_activities(self, date):
        week_activities = self.get_week_activities(date)

        return [activity for activity in week_activities if activity.status == "Pendiente"]

    def get_day_activities(self, date):
        day_activities = []
        for activity in self.user.activities:
            if activity.due_date.isocalendar() == date.isocalendar():
                day_activities.append(activity)
        
        return day_activities

    def get_week_production(self, date):
        weekday_dates = MyCalendar.get_weekday_dates(date)
        week_production = []
        for day in weekday_dates.values():
            day_production = self.get_day_production(day)
            week_production += day_production
        
        return week_production

    def get_day_production(self, date):
        day_production = []
        for production in self.user.production:
            if production.date.isocalendar() == date.isocalendar():
                day_production.append(production)
        
        return day_production
