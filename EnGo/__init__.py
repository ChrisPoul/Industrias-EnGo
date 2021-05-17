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

    from .models import db, init_db_command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    from .views import home
    app.register_blueprint(home.bp)

    from .views import auth
    app.register_blueprint(auth.bp)

    from .views import admin
    app.register_blueprint(admin.bp)

    from .views import product
    app.register_blueprint(product.bp)

    return app
