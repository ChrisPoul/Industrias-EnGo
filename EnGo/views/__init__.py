import functools
from flask import (
    request, g, redirect, url_for
)
from EnGo.models.view import View
from EnGo.models.permission import Permission


def permission_required(permission_name):
    def decorator(view_func):
        def wrapped_view(*args, **kwargs):
            permission = get_permission(permission_name)
            view_name = request.endpoint
            view = get_view(view_name, permission)
            user_permissions = get_user_permissions(g.user)
            if permission not in user_permissions:
                return redirect(
                    url_for('home.main_page')
                )
            return view_func(*args, **kwargs)

        return wrapped_view
    
    return decorator


def get_permission(name):
    permission = Permission.search(name)
    if not permission:
        permission = Permission(
            name=name
        )
        permission.add()
    
    return permission


def get_view(name, permission):
    view = View.search(name)
    if not view:
        view = View(
            name=name,
            permission_id=permission.id
        )
        view.add()

    return view


def get_user_permissions(user):
    try:
        permissions = user.permissions
    except AttributeError:
        permissions = []

    return permissions
