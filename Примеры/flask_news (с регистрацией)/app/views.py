from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from . import app, db
from .forms import NewsForm, LoginForm, RegistrationForm
from .models import Category, News, User


@app.route('/')
def index():
    news_list = News.query.order_by(News.created_date).all()
    categories = Category.query.all()
    return render_template('index.html',
                           news=news_list[::-1],
                           categories=categories)


@app.route('/news_detail/<int:id>')
def news_detail(id):
    news = News.query.get(id)
    categories = Category.query.all()
    return render_template('news_detail.html',
                           news=news,
                           categories=categories)


@app.route('/category/<int:id>')
def news_in_category(id):
    category = Category.query.get(id)
    news = category.news
    category_name = category.title
    categories = Category.query.all()
    return render_template('category.html',
                           news=news,
                           category_name=category_name,
                           categories=categories)


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        news = News()
        news.title = form.title.data
        news.text = form.text.data
        news.category_id = form.category.data
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('news_detail', id=news.id))
    return render_template('add_news.html',
                           form=form,
                           categories=categories)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
    return render_template('login.html', form=form, categories=categories)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    categories = Category.query.all()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form, categories=categories)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))