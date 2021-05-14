import functools
from flask import (
    request, g, redirect, url_for
)
from EnGo.models.view import View
from EnGo.models.permission import Permission


def permission_required(permission_name):
    def decorator(view_func):
        def wrapped_view(*args, **kwargs):
            view_name = request.endpoint
            view = View.search(view_name)
            permission = Permission.search(permission_name)
            if not permission:
                permission = Permission(
                    name=permission_name
                )
                permission.add()
            if not view:
                view = View(
                    name=view_name,
                    permission_id=permission.id
                )
                view.add()
            if permission not in g.user.permissions:
                return redirect(
                    url_for('home.main_page')
                )
            return view_func(*args, **kwargs)

        return wrapped_view
    
    return decorator

