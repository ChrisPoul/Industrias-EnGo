from datetime import datetime
from flask import (
    Blueprint, render_template, request,
    flash, redirect, url_for, g, session
)
from EnGo.models.user import User, UserActivity, UserProduction
from EnGo.models.calendar import MyCalendar
from . import (
    permission_required, login_required,
    get_checked_permissions, get_form,
    update_obj_attrs
)

bp = Blueprint("user", __name__, url_prefix="/user")

username_head = dict(
    username="Nombre de Usuario"
)
user_login_heads = dict(
    username_head,
    password="Contraseña"
)
user_heads = dict(
    user_login_heads,
    salary="Salario Mensual"
)
password_heads = dict(
    password="Escribe una contraseña...",
    password_confirm="Confirma la contraseña..."
)
weekday_heads = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}
activity_heads = dict(
    title="Título",
    description="Descripción",
    due_date="Fecha De Entrega"
)
production_heads = dict(
    concept="Concepto",
    quantity="Cantidad",
    date="Fecha de Registro"
)
permissions = [
    "Recursos Humanos"
]


@bp.route("/users", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def users():
    users = User.query.all()
    if request.method == "POST":
        user = User.search(request.form['search_term'])
        if user:
            return redirect(
                url_for('user.profile', id=user.id)
            )

    return render_template(
        "user/users.html",
        user_heads=username_head,
        users=users
    )


@bp.route("/register", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def register():
    form = get_form(user_heads)
    if request.method == "POST":
        error = None
        if form["password"] != request.form["password_confirm"]:
            error = "Las contraseñas no coinciden"
        if not error:
            user = User(
                username=form['username'],
                password=form['password'],
                salary=form['salary']
            )
            error = user.request.register()
        if not error:
            checked_permissions = get_checked_permissions()
            user.add_permissions(checked_permissions)
            return redirect(
                url_for('user.users')
            )
        flash(error)

    return render_template(
        "user/register.html",
        user_heads=user_heads,
        password_heads=password_heads,
        form=form
    )


@bp.route("/login", methods=('POST', 'GET'))
def login():
    if g.user:
        return redirect(
            url_for('home.main_page')
        )
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        error = user.request.login()
        if not error:
            return redirect(
                url_for('home.main_page')
            )
        flash(error)

    return render_template(
        "user/login.html",
        user_heads=user_login_heads
    )


@bp.route("/update/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update(id):
    user = User.get(id)
    user_heads = dict(
        username_head,
        salary="Salario"
    )
    if request.method == "POST":
        user.username = request.form["username"]
        user.salary = request.form['salary']
        checked_permissions = get_checked_permissions()
        user.update_permissions(checked_permissions)
        error = user.request.update()
        if not error:
            return redirect(
                url_for('user.users')
            )
        flash(error)

    return render_template(
        "user/update.html",
        user_heads=user_heads,
        user=user
    )


@bp.route("/update_password/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_password(id):
    user = User.get(id)
    if request.method == "POST":
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        if password != password_confirm:
            error = "Las contraseñas no coinciden"
        else:
            user.password = password
            error = user.validation.validate()
        if not error:
            from werkzeug.security import generate_password_hash
            user.password = generate_password_hash(user.password)
            user.update()
            return redirect(
                url_for('user.update', id=id)
            )
        flash(error)
    
    return render_template(
        'user/update_password.html',
        password_heads=password_heads,
        user=user
    )


@bp.route("/logout")
@login_required
def logout():
    session.clear()

    return redirect(
        url_for("user.login")
    )


@bp.route("/delete/<int:id>")
@permission_required(permissions)
@login_required
def delete(id):
    user = User.get(id)
    user.delete()

    return redirect(
        url_for('user.users')
    )


@bp.before_app_request
def load_loged_in_user():
    try:
        user_id = session["user_id"]
    except KeyError:
        user_id = None

    if user_id is None:
        g.user = None
    else:
        g.user = User.get(user_id)


@bp.route("/profile/<int:id>", methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def profile(id):
    user = User.query.get(id)
    selected_date = datetime.today()
    selected_week_str = selected_date.strftime("%Y-W%W")
    if request.method == "POST":
        selected_week_str = request.form["selected_week"]
        selected_date = datetime.strptime(selected_week_str + "-1", "%Y-W%W-%w")
    week_activities = user.schedule.get_weekday_activities(selected_date)
    week_production = user.schedule.get_week_production(selected_date)
    weekday_dates = MyCalendar.get_weekday_dates(selected_date)

    return render_template(
        "user/profile.html",
        weekday_heads=weekday_heads,
        production_heads=production_heads,
        week_activities=week_activities,
        weekday_dates=weekday_dates,
        user_production=week_production,
        selected_week_str=selected_week_str,
        user=user
    )


@bp.route('/day_activities/<int:id>/<string:date_str>')
@permission_required(permissions)
@login_required
def day_activities(id, date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    user = User.get(id)
    day_activities = user.schedule.get_day_activities(date)
    
    return render_template(
        'user/day-activities.html',
        user=user,
        activities=day_activities,
        date=date
    )


@bp.route("/assign_activity/<int:id>", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def assign_activity(id):
    min_date = datetime.today().strftime("%Y-%m-%d")
    if request.method == "POST":
        error = None
        due_date_str = request.form["due_date"]
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            error = "No has seleccionado una fecha, porfavor selecciona una"
        if not error:
            activity = UserActivity(
                user_id=id,
                title=request.form['title'],
                description=request.form['description'],
                due_date=due_date
            )
            error = activity.request.add()
        if not error:
            return redirect(
                url_for('user.profile', id=id)
            )
        flash(error)
        
    return render_template(
        "user/assign-activity.html",
        activity_heads=activity_heads,
        min_date=min_date
    )


@bp.route('/update_activity/<int:activity_id>', methods=('POST', 'GET'))
@permission_required(permissions)
@login_required
def update_activity(activity_id):
    activity = UserActivity.query.get(activity_id)
    activity_attrs = [
        "title",
        "description",
        "status"
    ]
    if request.method == "POST":
        update_obj_attrs(activity, activity_attrs)
        due_date_str = request.form['due_date']
        activity.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        error = activity.request.update()
        if not error:
            return redirect(
                url_for('user.profile', id=activity.user_id)
            )
        flash(error)

    return render_template(
        'user/update-activity.html',
        activity=activity
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
        "user/register-production.html",
        production_heads=production_heads
    )


@bp.route('/production/<int:user_id>')
@permission_required(permissions)
@login_required
def production(user_id):
    user = User.query.get(user_id)
    user_production = user.production

    return render_template(
        "user/production.html",
        production_heads=production_heads,
        user_production=user_production,
        user=user
    )
    
