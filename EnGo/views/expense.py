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
    'Contaduría'
]
expense_heads = dict(
    concept="Concepto",
    type="Tipo",
    cost="Costo"
)

@bp.route('/expenses')
@permission_required(permissions)
@login_required
def expenses():
    expenses = Expense.get_all()
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