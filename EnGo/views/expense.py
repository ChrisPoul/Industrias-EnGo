from flask import (
    Blueprint, render_template, redirect,
    request, url_for, flash
)
from EnGo.models.expense import Expense
from . import (
    login_required, permission_required, get_form,
    update_obj_attrs
)

bp = Blueprint('expense', __name__, url_prefix='/expense')

permissions = [
    'Dev'
]
expense_heads = dict(
    concept="Concepto",
    type="Tipo",
    cost="Costo"
)

@bp.route('/expenses', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def expenses():
    expenses = Expense.get_all()
    if request.method == "POST":
        search_term = request.form["search_term"]
        expense = Expense.search(search_term)
        if expense:
            return redirect(
                url_for('expense.update', id=expense.id)
            )
    return render_template(
        'expense/expenses.html',
        expense_heads=expense_heads,
        expenses=expenses
    )


@bp.route('/add', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add():
    form = get_form(expense_heads)
    if request.method == "POST":
        expense = Expense(
            concept=form['concept'],
            type=form['type'],
            cost=form['cost']
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
        form=form
    )


@bp.route('/update/<int:id>', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def update(id):
    expense = Expense.get(id)
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
        expense=expense
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