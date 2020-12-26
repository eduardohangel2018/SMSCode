import os
from flask import render_template, redirect, url_for, app, request, flash, abort, current_app
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from app.main.forms import LoginForm, RegistrationForm, EditProfileForm, EditProfileFormAdmin, TopicForm
from ..models import Role, User, Topic, Permission
from . import main
from .. import db
from werkzeug.utils import secure_filename
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(body=form.body.data,
                      author=current_user._get_current_object())
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Topic.query.order_by(Topic.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_TOPICS_PER_PAGE'], error_out=False)
    topics = pagination.items
    return render_template('index.html', form=form, topics=topics, pagination=pagination)


@main.route('/topic', methods=['GET', 'POST'])
@login_required
def topic():
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(body=form.body.data,
                      author=current_user._get_current_object())
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.topic'))
    page = request.args.get('page', 1, type=int)
    pagination = Topic.query.order_by(Topic.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_TOPICS_PER_PAGE'], error_out=False)
    topics = pagination.items
    return render_template('topics.html', form=form, topics=topics, pagination=pagination)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('main.login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.register(name=form.name.data,
                             username=form.username.data,
                             password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado com Sucesso')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.topics.order_by(Topic.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_TOPICS_PER_PAGE'], error_out=False)
    topics = pagination.items
    return render_template('user.html', user=user, topics=topics, pagination=pagination)


@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Seu perfil foi Atualizado')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


# @main.route('/edit/profile/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_profile_admin(id):
#     user = User.query.get_or_404(id)
#     form = EditProfileFormAdmin(user=user)
#     if form.validate_on_submit():
#         user.name = form.name.data
#         user.username = form.username.data
#         user.confirmed = form.confirmed.data
#         user.role = Role.query.get(form.role.data)
#         user.location = form.location.data
#         user.about_me = form.about_me.data
#         db.session.add(user)
#         db.session.commit()
#         flash('O Perfil foi atualizado')
#         return redirect(url_for('.user', username=user.username))
#     form.name.data = user.name
#     form.username.data = user.username
#     form.confirmed.data = user.confirmed
#     form.role.data = user.role_id
#     form.location.data = user.location
#     form.about_me.data = user.about_me
#     return render_template('edit_profile.html', form=form, user=user)


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
