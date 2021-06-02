import os
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, current_app
)
from EnGo.models.permission import Permission
from EnGo.models.view import View
from EnGo.commands.settings import get_settings, save_settings
from . import get_checked_permissions


bp = Blueprint('view', __name__, url_prefix="/view")


@bp.route('/update/<int:id>', methods=("POST", "GET"))
def update(id):
    view = View.get(id)
    if request.method == "POST":
        try:
            receipt_image = request.files["receipt_image"]
        except KeyError:
            receipt_image = None
        if receipt_image:
            save_image(receipt_image)
        checked_permissions = get_checked_permissions()
        view.update_permissions(checked_permissions)
        try:
            url = session["prev_url"]
        except KeyError:
            url = url_for('home.main_page')

        return redirect(
            url
        )

    return render_template(
        'view/update.html',
        view=view
    )


def save_image(image_file):
    receipt_image = os.path.join("images", image_file.filename)
    image_path = os.path.join(current_app.static_folder, receipt_image)
    image_file.save(image_path)
    settings = get_settings()
    settings["receipt_image"] = receipt_image
    save_settings(settings)


view_heads = {
    "admin.main_page": "Página del Administrador",
    "customer.add": "Página de Añadir Cliente",
    "customer.update": "Página de Editar Cliente",
    "customer.customers": "Página de Clientes",
    "customer.receipts": "Página de Recibos del Cliente",
    "customer.delete": "Página de Eliminar Cliente",
    "product.add": "Página de Añadir Producto",
    "product.update": "Página de Editar Producto",
    "product.products": "Página de Productos",
    "product.delete": "Página de Eliminar Producto",
    "receipt.add": "Página de Añadir Recibo",
    "receipt.edit": "Página de Editar Recibo",
    "receipt.done": "Página de Recibo Terminado",
    "receipt.remove_product": "Página de Eliminar Producto del Recibo",
    "receipt.delete": "Página de Eliminar Recibo",
    "user.register": "Página de Añadir Empleado",
    "user.update": "Página de Editar Empleado",
    "user.update_password": "Página de Editar Contraseña del Empleado",
    "user.users": "Página de Empleados",
    "user.delete": "Página de Eliminar Empleado"
}
