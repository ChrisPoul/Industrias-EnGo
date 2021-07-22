from datetime import datetime
from flask import (
    render_template, request,
    flash, redirect, url_for
)
from EnGo.models.user import User, UserProduction
from EnGo.views import (
    permission_required, login_required
)
from . import bp

production_heads = dict(
    concept="Concepto",
    quantity="Cantidad",
    date="Fecha de Registro"
)
permissions = [
    "Recursos Humanos"
]


@bp.route('/production/<int:user_id>', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def production(user_id):
    user = User.query.get(user_id)
    user_production = user.production
    selected_date_str = ""
    if request.method == "POST":
        selected_date_str = request.form['selected_date']
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
        user_production = user.schedule.get_day_production(selected_date)

    return render_template(
        "user/production/production.html",
        production_heads=production_heads,
        selected_date_str=selected_date_str,
        user_production=user_production,
        user=user
    )


@bp.route('/register_production/<int:user_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register_production(user_id):
    if request.method == "POST":
        production = UserProduction(
            user_id=user_id,
            concept=request.form['concept'],
            quantity=request.form['quantity']
        )
        error = production.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=user_id)
            )
        flash(error)
    
    return render_template(
        "user/production/register-production.html",
        production_heads=production_heads
    )
