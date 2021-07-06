from datetime import date, timedelta
from . import UserTest
from EnGo.models.user import User, UserActivity, UserProduction


class UserScheduleTest(UserTest):
    
    def setUp(self):
        UserTest.setUp(self)
        self.user_production = UserProduction(
            user_id=self.user.id,
            concept="Test Production",
            quantity=10,
            date=date.today()
        )
        self.user_production.add()
        user_production2 = UserProduction(
            user_id=self.user.id,
            concept="Test Production",
            quantity=10,
            date=date.today() + timedelta(days=10)
        )
        user_production2.add()
        self.user_activity = UserActivity(
            user_id=self.user.id,
            title="Test Activity",
            due_date=date.today()
        )
        self.user_activity.add()
        user_activity2 = UserActivity(
            user_id=self.user.id,
            title="Test Activity",
            due_date=date.today() + timedelta(days=10)
        )
        user_activity2.add()


class TestGetDayActivities(UserScheduleTest):

    def test_should_return_all_activities_scheduled_for_the_given_day(self):
        day_activities = self.user.schedule.get_day_activities(date.today())

        self.assertEqual(day_activities, [self.user_activity])

    def test_should_return_empty_list_given_no_activities_scheduled_for_the_given_day(self):
        day_activities = self.user.schedule.get_day_activities(date.today() + timedelta(days=1))

        self.assertEqual(day_activities, [])


class TestGetWeekdayActivities(UserScheduleTest):

    def test_should_return_all_week_activities_ordered_by_weekday_scheduled_for_given_week(self):
        weekday_activities = self.user.schedule.get_weekday_activities(date.today())
        activities = []
        for day_activities in weekday_activities.values():
            activities += day_activities

        self.assertEqual(activities, [self.user_activity])

    def test_should_not_return_activities_given_no_activities_scheduled_for_given_week(self):
        weekday_activities = self.user.schedule.get_weekday_activities(date.today() - timedelta(days=10))
        activities = []
        for day_activities in weekday_activities.values():
            activities += day_activities

        self.assertEqual(activities, [])


class TestGetDayProduction(UserScheduleTest):

    def test_should_return_all_production_registered_on_given_date(self):
        day_production = self.user.schedule.get_day_production(date.today())

        self.assertEqual(day_production, [self.user_production])

    def test_should_return_empty_list_given_no_production_registered_on_given_date(self):
        day_production = self.user.schedule.get_day_production(date.today() - timedelta(days=10))

        self.assertEqual(day_production, [])


class TestGetWeekProduction(UserScheduleTest):

    def test_should_return_all_production_registered_on_given_week(self):
        week_production = self.user.schedule.get_week_production(date.today())

        self.assertEqual(week_production, [self.user_production])

    def test_should_return_empty_list_given_no_production_registered_on_given_week(self):
        week_production = self.user.schedule.get_week_production(date.today() - timedelta(days=10))

        self.assertEqual(week_production, [])
