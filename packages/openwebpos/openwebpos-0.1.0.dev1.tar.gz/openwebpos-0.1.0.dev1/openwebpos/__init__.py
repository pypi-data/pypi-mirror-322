from flask import Flask

from .manage import add_cli_commands
from .urls import register_routes


def create_app():
    app = Flask(__name__, template_folder="ui/templates", static_folder="ui/static")

    app.config.from_pyfile("config.py")

    app.config.from_envvar("OPENWEBPOS_SETTINGS", silent=True)

    init_extensions(app)

    add_cli_commands(app)

    custom_jinja_filters(app)

    register_routes(app)

    return app


def init_extensions(app):
    from .extensions import db, login_manager
    from openwebpos.blueprints.user.models.user import User

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "user.login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))


def custom_jinja_filters(app):
    datetime_formats = {
        "short-date": "%y-%m-%d",
        "full-date": "%Y-%m-%d",
        "time": "%I:%M %p",
        "time-24": "%H:%M",
        "datetime": "%Y-%m-%d %H:%M:%S",
    }
    default_datetime_format = app.config["DATETIME_FORMAT"]

    @app.template_filter("datetime")
    def format_datetime(value, format_spec=default_datetime_format):
        if format_spec in datetime_formats:
            format_spec = datetime_formats[format_spec]
        return value.strftime(format_spec)

    @app.template_filter("currency")
    def format_currency(value):
        return f"${value:.2f}"

    @app.template_filter("phone")
    def format_phone(value):
        return f"({value[:3]}) {value[3:6]}-{value[6:]}"
