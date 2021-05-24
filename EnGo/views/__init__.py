import functools
from flask import (
    request, g, redirect, url_for
)
from EnGo.models.view import View
from EnGo.models.permission import Permission


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(
                url_for('user.login')
            )
        return view(**kwargs)

    return wrapped_view


def permission_required(permission_names):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(*args, **kwargs):
            view_name = request.endpoint
            set_view_permissions(view_name, permission_names)
            if not g.user or g.user.has_permission(view_name) is False:
                return redirect(
                    url_for('home.main_page')
                )
            return view_func(*args, **kwargs)

        return wrapped_view
    
    return decorator


def set_view_permissions(view_name, permission_names):
    view = View.search(view_name)
    permissions = get_permissions(permission_names)
    if not view:
        view = View(
            view_name=view_name
        )
        view.add()
        view.add_permissions(permissions)
    if view.permissions != permissions:
        view.update_permissions()


def get_permissions(names):
    permissions = []
    for name in names:
        permission = get_permission(name)
        permissions.append(permission)
    
    return permissions


def get_permission(name):
    permission = Permission.search(name)
    if not permission:
        permission = Permission(
            permission_name=name
        )
        permission.add()
    
    return permission


def update_obj_attrs(obj, heads):
    for attribute in heads:
        update_obj_attr(obj, attribute)


def update_obj_attr(obj, attribute):
    try:
        value = request.form[attribute]
        setattr(obj, attribute, value)
    except KeyError:
        pass


def get_form(heads):
    form = {}
    for key in heads:
        try:
            value = request.form[key]
        except KeyError:
            value = ""
        form[key] = value

    return form


def get_empty_form(heads):
    form = {}
    for key in heads:
        form[key] = ""

    return form


def format_price(price, iva=None):
    price = float(price)
    if iva:
        price = price * iva
    price = round(price, 2)
    price = str(price)
    price_int, price_dec = price.split(".")
    price_int = add_comma_separators_to_num(price_int)
    price_dec = format_decimal_of_price(price_dec)
    formated_price = f"${price_int}.{price_dec}"

    return formated_price


def add_comma_separators_to_num(num):
    num = str(num)
    formated_num = ""
    for i, digit in enumerate(num[::-1], start=1):
        formated_num += digit
        if i % 3 == 0:
            formated_num += ","
    formated_num = formated_num[::-1]

    return formated_num


def format_decimal_of_price(decimal):
    if len(decimal) == 1:
        decimal += "0"
    return decimal
