import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app.instance_path}/EnGo.db"

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db, init_db_command
    db.init_app(app)
    app.cli.add_command(init_db_command)

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

    return app
