from flask import (
    Blueprint, render_template, request,
    url_for, redirect, flash
)
from EnGo.models.post import Post
from . import (
    permission_required, login_required,
    update_obj_attrs, get_form
)

bp = Blueprint("post", __name__, url_prefix="/post")

post_heads = dict(
    title="Título",
    description="Descripción"
)
permissions = [
    "Admin"
]


@bp.route("/add", methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def add():
    if request.method == "POST":
        post = Post(
            title=request.form["title"],
            description=request.form["description"]
        )
        error = post.request.add()
        if not error:
            return redirect(
                url_for('home.main_page')
            )
        flash(error)
        
    return render_template(
        'post/add.html',
        post_heads=post_heads
    )


@bp.route('/update/<int:id>', methods=("POST", "GET"))
@permission_required(permissions)
@login_required
def update(id):
    post = Post.get(id)
    if request.method == "POST":
        update_obj_attrs(post, post_heads)
        error = post.request.update()
        if not error:
            return redirect(
                url_for('home.main_page')
            )
        flash(error)

    return render_template(
        'post/update.html',
        post_heads=post_heads,
        post=post
    )

@bp.route('/delete/<int:id>')
@permission_required(permissions)
@login_required
def delete(id):
    post = Post.get(id)
    post.delete()

    return redirect(
        url_for('home.main_page')
    )