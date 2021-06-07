from . import ExpenseTest
from flask import url_for
from EnGo.models.expense import Expense, ExpenseType

### LOGED IN USER HAS PERMISSISON (LUHP) ###
### LOGED IN USER HAS NO PERMISSION (LUHNP) ###


class ExpenseViewTest(ExpenseTest):

    def setUp(self):
        ExpenseTest.setUp(self)
        self.create_test_users()


class TestExpensesView(ExpenseViewTest):

    def test_should_return_valid_response_given_LUHP(self):
        self.login_user(self.dev_user)
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

    def test_should_add_expense_given_valid_expense_input_and_LUHP(self):
        self.login_user(self.dev_user)
        expense_input = dict(
            concept="Valid Concept",
            type_id=self.expense_type.id,
            cost=10,
            unit="pz",
            quantity=10
        )
        with self.client as client:
            client.post(
                url_for('expense.add'),
                data=expense_input
            )
        
        self.assertEqual(len(Expense.search_all("Valid Concept")), 1)
    
    def test_should_not_add_expense_given_invalid_expense_input_and_LUHP(self):
        self.login_user(self.dev_user)
        expense_input = dict(
            concept="Some Expense",
            type_id=self.expense_type.id,
            cost=10,
            unit="pz",
            quantity=""
        )
        with self.client as client:
            client.post(
                url_for('expense.add'),
                data=expense_input
            )
        
        self.assertEqual(len(Expense.search_all('Some Expense')), 0)
    
    def test_should_redirect_given__LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('expense.add')
            )
        
        self.assertStatus(response, 302)


class TestUpdateView(ExpenseViewTest):

    def test_should_update_expense_given_valid_expense_input_and_LUHP(self):
        self.login_user(self.dev_user)
        expense_data = dict(
            concept="New Concept",
            type_id=self.expense_type.id,
            cost=10,
            unit="pz",
            quantity=10
        )
        with self.client as client:
            client.post(
                url_for('expense.update', id=self.expense.id),
                data=expense_data
            )
        self.db.session.rollback()

        self.assertEqual(self.expense.concept, "New Concept")
    
    def test_should_not_update_expense_given_invalid_expense_input_and_LUHP(self):
        self.login_user(self.dev_user)
        expense_input = dict(
            concept="New Concept",
            type_id=self.expense_type.id,
            cost=10,
            unit="pz",
            quantity=""
        )
        with self.client as client:
            client.post(
                url_for('expense.update', id=self.expense.id),
                data=expense_input
            )
        self.db.session.rollback()

        self.assertNotEqual(self.expense.concept, "New Concept")
    
    def test_should_redirect_given_LUHNP(self):
        self.login_user(self.normal_user)
        with self.client as client:
            response = client.get(
                url_for('expense.update', id=self.expense.id)
            )
        
        self.assertStatus(response, 302)


class AddType(ExpenseViewTest):

    def test_should_add_expense_type_given_valid_type_input_and_LUHP(self):
        self.login_user(self.dev_user)
        type_input = dict(
            name="New Expense Type"
        )
        with self.client as client:
            client.post(
                url_for('expense.add_type'),
                data=type_input
            )
        
        self.assertTrue(ExpenseType.search("New Expense Type"))


class TestDeleteView(ExpenseViewTest):
    
    def test_should_delete_expense_given_LUHP(self):
        self.login_user(self.dev_user)
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

