from flask import Blueprint
from flask import render_template, request, redirect, url_for
from app.models import Post
from sqlalchemy import or_

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/search')
def search():
    search_query = request.args.get('query')
    if search_query is None or search_query=="":
        return redirect(url_for('main.home'))
    # Perform search using SQLAlchemy
    search_results = Post.query.filter(\
        or_(Post.title.contains(search_query), Post.content.contains(search_query))\
            ).order_by(Post.date_posted.desc()).all()
    return render_template('search_results.html', posts=search_results, search_query=search_query)
        