from flask import Blueprint, flash, render_template, url_for, redirect, abort, request
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.posts.forms import PostForm, CommentForm
from flaskblog.models import Post, Comment

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            city=form.city.data,
            content=form.content.data,
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.home"))

    return render_template(
        "new_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>/comments/new", methods=["POST", "GET"])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post=post,
            author=current_user,
        )
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added!", "success")
        return redirect(url_for("posts.post", post_id=post_id))

    return render_template(
        "new_comment.html",
        title="New Comment",
        form=form,
        legend="New Comment - " + post.title,
    )


@posts.route(
    "/post/<int:post_id>/comments/<int:comment_id>/delete", methods=["POST", "GET"]
)
@login_required
def delete_comment(comment_id, post_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    flash("Your comment has been deleted!", "success")
    return redirect(url_for("posts.post", post_id=post_id))


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post=post).order_by(Comment.date_posted.desc())
    return render_template(
        "post.html",
        title=post.title,
        post=post,
        comments=comments,
    )


@posts.route("/post/<int:post_id>/update", methods=["POST", "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.city = form.city.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")

        return redirect(url_for("posts.post", post_id=post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template(
        "new_post.html", title="Update Post", form=form, legend="Update Post", post=post
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
