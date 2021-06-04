from . import ExpenseTest
from flask import url_for
from EnGo.models.expense import Expense

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ExpenseViewTest(ExpenseTest):

    def setUp(self):
        ExpenseTest.setUp(self)
        self.create_test_users()


class TestExpensesView(ExpenseViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            response = client.get(
                url_for('expense.expenses')
            )
        
        self.assert200(response)

    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('expense.expenses')
            )
        
        self.assertStatus(response, 302)

class TestAddView(ExpenseViewTest):

    def test_should_add_expense_given_valid_expense_and_LUHP(self):
        self.login_user(self.admin_user)
        expense_data = dict(
            concept="Valid Concept",
            type="Valid Type",
            cost=10
        )
        with self.client as client:
            client.post(
                url_for('expense.add'),
                data=expense_data
            )
        
        self.assertTrue(Expense.search("Valid Concept"))
    
    def test_should_not_add_expense_given_invalid_expense_and_LUHP(self):
        self.login_user(self.admin_user)
        expense_data = dict(
            concept="Valid Concept",
            type="",
            cost=10
        )
        with self.client as client:
            client.post(
                url_for('expense.add'),
                data=expense_data
            )
        
        self.assertFalse(Expense.search('Valid Concept'))
    
    def test_should_redirect_given__LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('expense.add')
            )
        
        self.assertStatus(response, 302)


class TestUpdateView(ExpenseViewTest):

    def test_should_update_expense_given_valid_change_and_LUHP(self):
        self.login_user(self.admin_user)
        expense_data = dict(
            concept="New Concept",
            type="Test Type"
        )
        with self.client as client:
            client.post(
                url_for('expense.update', id=self.expense.id),
                data=expense_data
            )
        self.db.session.rollback()

        self.assertEqual(self.expense.concept, "New Concept")
    
    def test_should_not_update_expense_given_invalid_change_and_LUHP(self):
        self.login_user(self.admin_user)
        expense_data = dict(
            concept="",
            type="Test Type"
        )
        with self.client as client:
            client.post(
                url_for('expense.update', id=self.expense.id),
                data=expense_data
            )
        self.db.session.rollback()

        self.assertNotEqual(self.expense.concept, "")
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('expense.update', id=self.expense.id)
            )
        
        self.assertStatus(response, 302)


class TestDeleteView(ExpenseViewTest):
    
    def test_should_delete_expense_given_LUHP(self):
        self.login_user(self.admin_user)
        with self.client as client:
            client.get(
                url_for('expense.delete', id=self.expense.id)
            )
        
        self.assertFalse(Expense.get(self.expense.id))
    
    def test_should_not_delete_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            client.get(
                url_for('expense.delete', id=self.expense.id)
            )
        
        self.assertTrue(Expense.get(self.expense.id))

