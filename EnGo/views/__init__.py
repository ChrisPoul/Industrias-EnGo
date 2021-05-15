import functools
from flask import (
    request, g, redirect, url_for
)
from EnGo.models.view import View, ViewPermission
from EnGo.models.permission import Permission


def permission_required(permission_names):
    def decorator(view_func):
        def wrapped_view(*args, **kwargs):
            view_name = request.endpoint
            set_view_permissions(view_name, permission_names)
            if g.user.has_permission(view_name):
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
            name=view_name
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
            name=name
        )
        permission.add()
    
    return permission
