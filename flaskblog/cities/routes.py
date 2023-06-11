from flask import Blueprint, flash, render_template, url_for, redirect, abort, request
from flaskblog.models import Post

cities = Blueprint("cities", __name__)


@cities.route("/cities/<string:city>")
def cities_posts(city):
    page = request.args.get("page", 1, type=int)
    # posts = Post.query.filter_by(city=city).first_or_404()
    posts = (
        Post.query.filter_by(city=city)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("city_posts.html", posts=posts, city=city)
