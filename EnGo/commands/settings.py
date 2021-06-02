import os
import json
import click
from flask import current_app
from flask.cli import with_appcontext


@click.command("init-settings")
@with_appcontext
def init_settings_command():
    init_settings()
    click.echo("Initialized Settings")


def init_settings():
    settings = dict(
        receipt_image="images/logo.jpeg"
    )
    save_settings(settings)


def save_settings(settings):
    settings_path = os.path.join(current_app.instance_path, "settings.json")
    with open(settings_path, "w+") as settings_file:
        json.dump(settings, settings_file, indent=4)


def get_settings():
    settings_path = os.path.join(current_app.instance_path, "settings.json")
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)

    return settings