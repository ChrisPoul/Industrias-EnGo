from flask import (
    Blueprint, render_template, redirect,
    request, url_for, flash
)
from EnGo.models.expense import (
    Expense, ExpenseType, filter_expenses_by_type
) 
from . import (
    login_required, permission_required, get_form,
    update_obj_attrs
)

bp = Blueprint('expense', __name__, url_prefix='/expense')

permissions = [
    'Contaduría'
]
expense_heads = dict(
    concept="Concepto",
    type_id="Tipo",
    quantity="Cantidad",
    unit="Unidad",
    cost="Costo"
)


@bp.route('/expenses', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def expenses():
    expenses = Expense.get_all()
    expense_types = ExpenseType.query.all()
    selected_expense_type = dict (
        id=0,
        name="Todos"
    )
    expense_types.append(selected_expense_type)
    if request.method == "POST":
        search_term = request.form["search_term"]
        if search_term != "":
            expenses = Expense.search_all(search_term)
        type_id = int(request.form['type_id'])
        if type_id != 0:
            selected_expense_type = ExpenseType.query.get(type_id)
        expenses = filter_expenses_by_type(expenses, type_id)
            
    return render_template(
        'expense/expenses.html',
        expense_heads=expense_heads,
        expenses=expenses,
        expense_types=expense_types,
        selected_expense_type=selected_expense_type
    )


@bp.route('/add', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add():
    expense_types = ExpenseType.query.all()
    if request.method == "POST":
        expense = Expense(
            concept=request.form['concept'],
            type_id=request.form['type_id'],
            cost=request.form['cost'],
            unit=request.form['unit'],
            quantity=request.form['quantity']
        )
        error = expense.request.add()
        if not error:
            return redirect(
                url_for('expense.expenses')
            )
        flash(error)

    return render_template(
        'expense/add.html',
        expense_heads=expense_heads,
        expense_types=expense_types
    )


@bp.route('/update/<int:id>', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def update(id):
    expense = Expense.get(id)
    expense_types = ExpenseType.query.all()
    if request.method == "POST":
        update_obj_attrs(expense, expense_heads)
        error = expense.request.update()
        if not error:
            return redirect(
                url_for('expense.expenses')
            )
        flash(error)
    
    return render_template(
        'expense/update.html',
        expense_heads=expense_heads,
        expense_types=expense_types,
        expense=expense
    )


@bp.route('/add_type', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def add_type():
    form = get_form(["name"])
    if request.method == "POST":
        expense_type = ExpenseType(
            name=form["name"]
        )
        error = expense_type.request.add()
        if not error:
            return redirect(
                url_for('expense.add')
            )
        flash(error)
    
    return render_template(
        'expense/add_type.html'
    )


@bp.route('/delete/<int:id>')
@permission_required(permissions)
@login_required
def delete(id):
    expense = Expense.get(id)
    expense.delete()

    return redirect(
        url_for('expense.expenses')
    )