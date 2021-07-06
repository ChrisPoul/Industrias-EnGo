from EnGo.models.calendar import MyCalendar


class UserSchedule:

    def __init__(self, user):
        self.user = user

    def get_week_activities(self, date):
        week_activities = self.filter_activities_by_week(date)
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

    def get_day_production(self, date):
        day_production = []
        for production in self.user.production:
            production_date = production.date.date()
            if production_date == date:
                day_production.append(production)
        
        return day_production

    def get_week_production(self, date):
        weekday_dates = MyCalendar.get_weekday_dates(date)
        week_production = []
        for weekday in weekday_dates:
            date = weekday_dates[weekday].date()
            day_production = self.get_day_production(date)
            week_production += day_production
        
        return week_production

    def filter_activities_by_week(self, date):
        week_activities = []
        for activity in self.user.activities:
            selected_year, selected_week, _ = date.isocalendar()
            due_year, due_week, _ = activity.due_date.isocalendar()
            if due_year == selected_year and due_week == selected_week:
                week_activities.append(activity)
        
        return week_activities