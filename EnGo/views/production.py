from datetime import datetime
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for
)
from EnGo.models.user import User
from EnGo.models.production import Production
from EnGo.views import (
    permission_required, login_required
)

bp = Blueprint("production", __name__, url_prefix="/production")

production_heads = dict(
    concept="Concepto",
    quantity="Cantidad",
    user_id="Empleado",
    date="Fecha de Registro"
)
permissions = [
    "Recursos Humanos"
]


@bp.route('/production', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def production():
    user_production = Production.query.all()
    selected_date_str = ""
    if request.method == "POST":
        selected_date_str = request.form['selected_date']
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
        user_production = user.schedule.get_day_production(selected_date)

    return render_template(
        "production/production.html",
        production_heads=production_heads,
        selected_date_str=selected_date_str,
        user_production=user_production
    )


@bp.route('/register', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register():
    users = [user for user in User.query.all() if not user.is_admin()]
    selected_user = dict(
        id=0,
        username="Seleccionar Empleado"
    )
    if request.method == "POST":
        production = Production(
            user_id=request.form['user_id'],
            concept=request.form['concept'],
            quantity=request.form['quantity']
        )
        error = production.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=production.user_id)
            )
        flash(error)
    
    return render_template(
        "production/register.html",
        production_heads=production_heads,
        selected_user=selected_user,
        users=users
    )
