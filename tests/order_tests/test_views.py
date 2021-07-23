from datetime import date
from flask import url_for
from . import OrderTest
from EnGo.models.order import Order
from EnGo.models.user import User


class OrderViewTest(OrderTest):

    def setUp(self):
        OrderTest.setUp(self)
        self.create_test_users()
        self.user = User(
            username="Test User",
            password="0000",
        )
        self.user.add()


class TestAssignView(OrderViewTest):

    def test_should_assign_order_given_valid_order_input_and_LUHP(self):
        self.login_user(self.dev_user)
        order_input = dict(
            user_id=self.user.id,
            title="New Order",
            description="Test Description",
            due_date=date.today().strftime('%Y-%m-%d')
        )
        with self.client as client:
            client.post(
                url_for('order.assign'),
                data=order_input
            )
        
        self.assertEqual(len(self.user.orders), 1)
    
    def test_should_not_assign_order_given_invalid_title_and_LUHP(self):
        self.login_user(self.dev_user)
        order_input = dict(
            user_id=self.user.id,
            title="",
            description="Test Description",
            due_date=date.today().strftime('%Y-%m-%d')
        )
        with self.client as client:
            client.post(
                url_for('order.assign'),
                data=order_input
            )
        
        self.assertEqual(len(self.user.orders), 0)
    
    def test_should_not_assign_order_given_invalid_due_date_and_LUHP(self):
        self.login_user(self.dev_user)
        order_input = dict(
            user_id=self.user.id,
            title="Test Title",
            description="Test Description",
            due_date=""
        )
        with self.client as client:
            client.post(
                url_for('order.assign'),
                data=order_input
            )
        
        self.assertEqual(len(self.user.orders), 0)
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('order.assign')
            )
        
        self.assertStatus(response, 302)
    

class TestUpdateView(OrderViewTest):

    def test_should_update_order_given_valid_order_input_and_LUHP(self):
        self.login_user(self.dev_user)
        order_input = dict(
            user_id=self.user.id,
            title="New Title",
            description="Test Description",
            due_date=date.today().strftime("%Y-%m-%d")
        )
        with self.client as client:
            client.post(
                url_for('order.update', order_id=self.order.id),
                data=order_input
            )
        self.db.session.rollback()

        self.assertEqual(self.order.title, "New Title")
    
    def test_should_not_update_order_given_invalid_order_input_and_LUHP(self):
        self.login_user(self.dev_user)
        order_input = dict(
            user_id=self.user.id,
            title="",
            description="Test Description",
            due_date=date.today().strftime("%Y-%m-%d")
        )
        with self.client as client:
            client.post(
                url_for('order.update', order_id=self.order.id),
                data=order_input
            )
        self.db.session.rollback()

        self.assertNotEqual(self.order.title, "")

    def test_should_not_update_order_given_invalid_due_date_and_LUHP(self):
        self.login_user(self.dev_user)
        order_input = dict(
            user_id=self.user.id,
            title="New Title",
            description="Test Description",
            due_date=""
        )
        with self.client as client:
            client.post(
                url_for('order.update', order_id=self.order.id),
                data=order_input
            )
        self.db.session.rollback()

        self.assertNotEqual(self.order.due_date, "")

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for("order.update", order_id=self.user.id)
            )

        self.assertStatus(response, 302)
    

class TestDayOrdersView(OrderViewTest):

    def test_should_grant_access_given_LUHP(self):
        self.login_user(self.dev_user)
        date_str = date.today().strftime("%Y-%m-%d")
        with self.client as client:
            response = client.get(
                url_for("order.day_orders", user_id=self.user.id, date_str=date_str)
            )
        
        self.assert200(response)
    
    def test_should_not_grant_access_LUHP(self):
        self.login_user(self.normal_user)
        date_str = date.today().strftime("%Y-%m-%d")
        with self.client as client:
            response = client.get(
                url_for("order.day_orders", user_id=self.user.id, date_str=date_str)
            )
        
        self.assertStatus(response, 302)

