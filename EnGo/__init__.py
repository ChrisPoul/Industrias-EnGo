import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.instance_path}/EnGo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "dev"

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)

    from .commands import database, settings
    app.cli.add_command(database.init_db_command)
    app.cli.add_command(database.update_db_command)
    app.cli.add_command(settings.init_settings_command)

    from .views import global_context
    app.register_blueprint(global_context.bp)

    from . import errors
    app.register_blueprint(errors.bp)

    from .views import home
    app.register_blueprint(home.bp)

    from .views import user
    app.register_blueprint(user.bp)

    from .views import admin
    app.register_blueprint(admin.bp)

    from .views import view
    app.register_blueprint(view.bp)

    from .views import product
    app.register_blueprint(product.bp)

    from .views import customer
    app.register_blueprint(customer.bp)

    from .views import receipt
    app.register_blueprint(receipt.bp)

    from .views import warehouse
    app.register_blueprint(warehouse.bp)

    from .views import post
    app.register_blueprint(post.bp)

    from .views import expense
    app.register_blueprint(expense.bp)

    from .views import calendar
    app.register_blueprint(calendar.bp)

    from .views import order
    app.register_blueprint(order.bp)

    from .views import activity
    app.register_blueprint(activity.bp)

    from .views import production
    app.register_blueprint(production.bp)

    return app
