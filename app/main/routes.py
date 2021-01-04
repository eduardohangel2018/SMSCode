import os
from flask import render_template, redirect, url_for, app, request, flash, abort, current_app
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from app.main.forms import LoginForm, RegistrationForm, EditProfileForm, EditProfileFormAdmin, TopicForm, \
    ChangePasswordForm
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


@main.route('/topics', methods=['GET', 'POST'])
@login_required
def _topic():
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(body=form.body.data,
                      author=current_user._get_current_object())
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('main.topics'))
    page = request.args.get('page', 1, type=int)
    pagination = Topic.query.order_by(Topic.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_TOPICS_PER_PAGE'], error_out=False)
    topics = pagination.items
    return render_template('topics.html', form=form, topics=topics, pagination=pagination)


@main.route('/topic/<int:id>')
def topic(id):
    topic = Topic.query.get_or_404(id)
    return render_template('topic.html', topics=[topic])


@main.route('/edit_topic/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_topic(id):
    topic = Topic.query.get_or_404(id)
    if current_user != topic.author:
        abort(403)
    form = TopicForm()
    if form.validate_on_submit():
        topic.body = form.body.data
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('main.topic', id=topic.id))
    form.body.data = topic.body
    return render_template('edit_topic.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.register(name=form.name.data,
                             username=form.username.data,
                             password=form.password.data,)
        r = Role(name='User')
        r.add_permission(Permission.ADMIN)
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


@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileFormAdmin(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('O Perfil foi atualizado')
        return redirect(url_for('.user', form=form, username=user.username))
    form.name.data = user.name
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            current_user.password2 = form.password2.data
            flash('Sua senha foi alterada com sucesso')
            return redirect(url_for('main.index'))
        else:
            flash('Senha Inválida')
        return render_template('change_password.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        print(user.role)
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
