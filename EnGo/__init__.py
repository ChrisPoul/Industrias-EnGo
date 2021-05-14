from flask import Flask


def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:////{app.instance_path}/EnGo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "dev"

    from .models import db, init_db_command
    db.init_app(app)
    app.cli.add_command(init_db_command)

    from .views import home
    app.register_blueprint(home.bp)

    from .views import admin
    app.register_blueprint(admin.bp)

    return app
