import os
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, current_app
)
from EnGo.models.permission import Permission
from EnGo.models.view import View
from EnGo.commands.settings import get_settings, save_settings
from . import (
    login_required, permission_required,
    get_checked_permissions
)


bp = Blueprint('view', __name__, url_prefix="/view")


@bp.route('/update/<int:id>', methods=("POST", ))
@permission_required(["Admin"])
@login_required
def update(id):
    view = View.get(id)
    try:
        receipt_image = request.files["receipt_image"]
    except KeyError:
        receipt_image = None
    if receipt_image:
        save_image(receipt_image)
    checked_permissions = get_checked_permissions()
    view.update_permissions(checked_permissions)
    if not request.referrer:
        url = url_for('home.main_page')
    else:
        url = request.referrer

    return redirect(
        url
    )


def save_image(image_file):
    receipt_image = os.path.join("images", image_file.filename)
    image_path = os.path.join(current_app.static_folder, receipt_image)
    image_file.save(image_path)
    settings = get_settings()
    settings["receipt_image"] = receipt_image
    save_settings(settings)
