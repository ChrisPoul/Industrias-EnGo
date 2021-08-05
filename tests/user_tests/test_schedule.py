from datetime import date, timedelta
from . import UserTest
from EnGo.models.user import User
from EnGo.models.production import Production
from EnGo.models.activity import Activity
from EnGo.models.order import Order


class UserScheduleTest(UserTest):

    def setUp(self):
        UserTest.setUp(self)
        self.production = Production(
            user_id=self.user.id,
            concept="Test Production",
            quantity=10,
            date=date.today()
        )
        self.production.add()
        production2 = Production(
            user_id=self.user.id,
            concept="Test Production",
            quantity=10,
            date=date.today() + timedelta(days=10)
        )
        production2.add()
        self.activity = Activity(
            user_id=self.user.id,
            title="Test Activity"
        )
        self.activity.add()
        self.order = Order(
            user_id=self.user.id,
            title="Test Activity",
            status="Cancelada",
            due_date=date.today()
        )
        self.order.add()
        order2 = Order(
            user_id=self.user.id,
            title="Test Activity",
            status="Pendiente",
            due_date=date.today() + timedelta(days=10)
        )
        order2.add()


class TestGetDayActivities(UserScheduleTest):

    def test_should_return_all_activities_scheduled_for_the_given_day(self):
        day_activities = self.user.schedule.get_day_activities(date.today())

        self.assertEqual(day_activities, [self.activity])


class TestGetWeekdayActivities(UserScheduleTest):

    def test_should_return_all_week_activities_ordered_by_weekday_scheduled_for_given_week(self):
        weekday_activities = self.user.schedule.get_weekday_activities(
            date.today())
        activities = []
        for day_activities in weekday_activities.values():
            activities += day_activities

        self.assertEqual(activities, [self.activity])


class TestGetWeekActivities(UserScheduleTest):

    def test_should_return_all_week_activities_given_date(self):
        week_activities = self.user.schedule.get_week_activities(date.today())

        self.assertEqual(week_activities, [self.activity])


class TestGetDayOrders(UserScheduleTest):

    def test_should_return_all_orders_scheduled_for_the_given_day(self):
        day_orders = self.user.schedule.get_day_orders(date.today())

        self.assertEqual(day_orders, [self.order])

    def test_should_return_empty_list_given_no_orders_scheduled_for_the_given_day(self):
        day_orders = self.user.schedule.get_day_orders(
            date.today() + timedelta(days=1)
        )

        self.assertEqual(day_orders, [])


class TestGetWeekdayOrders(UserScheduleTest):

    def test_should_return_all_week_orders_ordered_by_weekday_scheduled_for_given_week(self):
        weekday_orders = self.user.schedule.get_weekday_orders(date.today())
        orders = []
        for day_orders in weekday_orders.values():
            orders += day_orders

        self.assertEqual(orders, [self.order])

    def test_should_not_return_orders_given_no_orders_scheduled_for_given_week(self):
        weekday_orders = self.user.schedule.get_weekday_orders(
            date.today() - timedelta(days=10))
        orders = []
        for day_orders in weekday_orders.values():
            orders += day_orders

        self.assertEqual(orders, [])


class TestGetWeekOrders(UserScheduleTest):

    def test_should_return_all_week_orders_given_date(self):
        week_orders = self.user.schedule.get_week_orders(date.today())

        self.assertEqual(week_orders, [self.order])

    def test_should_not_return_week_orders_given_no_orders_sheduled_for_given_week(self):
        week_orders = self.user.schedule.get_week_orders(
            date.today() - timedelta(days=10))

        self.assertEqual(week_orders, [])


class TestGetFinishedWeekOrders(UserScheduleTest):

    def setUp(self):
        UserScheduleTest.setUp(self)
        self.finished_order = Order(
            user_id=self.user.id,
            title="Test Activity",
            status="Completada",
            due_date=date.today()
        )
        self.finished_order.add()

    def test_should_return_all_finished_week_orders_given_date(self):
        week_finished_orders = self.user.schedule.get_finished_week_orders(
            date.today()
        )

        self.assertEqual(week_finished_orders, [self.finished_order])

    def test_should_not_return_finished_orders_given_no_orders_scheduled_for_given_week(self):
        week_finished_orders = self.user.schedule.get_finished_week_orders(
            date.today() - timedelta(days=10)
        )

        self.assertEqual(week_finished_orders, [])


class TestGetPendingWeekOrders(UserScheduleTest):

    def setUp(self):
        UserScheduleTest.setUp(self)
        self.pending_order = Order(
            user_id=self.user.id,
            title="Test Activity",
            status="Pendiente",
            due_date=date.today()
        )
        self.pending_order.add()

    def test_should_return_all_pending_week_orders_given_date(self):
        week_pending_orders = self.user.schedule.get_pending_week_orders(
            date.today())

        self.assertEqual(week_pending_orders, [self.pending_order])

    def test_should_not_return_pending_orders_given_no_orders_scheduled_for_given_week(self):
        week_pending_orders = self.user.schedule.get_pending_week_orders(
            date.today() - timedelta(days=10)
        )

        self.assertEqual(week_pending_orders, [])


class TestGetDayProduction(UserScheduleTest):

    def test_should_return_all_production_registered_on_given_date(self):
        day_production = self.user.schedule.get_day_production(date.today())

        self.assertEqual(day_production, [self.production])

    def test_should_return_empty_list_given_no_production_registered_on_given_date(self):
        day_production = self.user.schedule.get_day_production(
            date.today() - timedelta(days=10)
        )

        self.assertEqual(day_production, [])


class TestGetWeekProduction(UserScheduleTest):

    def test_should_return_all_production_registered_on_given_week(self):
        week_production = self.user.schedule.get_week_production(date.today())

        self.assertEqual(week_production, [self.production])

    def test_should_return_empty_list_given_no_production_registered_on_given_week(self):
        week_production = self.user.schedule.get_week_production(
            date.today() - timedelta(days=10))

        self.assertEqual(week_production, [])
