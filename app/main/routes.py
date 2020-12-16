import os
from flask import render_template, redirect, url_for, app, request, flash
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required, current_user
from app.main.forms import UploadForm, LoginForm, RegistrationForm
from ..models import db, User
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/topic', methods=['GET', 'POST'])
@login_required
def topic():
    image = None
    text = None
    form = UploadForm()
    if form.validate_on_submit():
        image = 'uploads/' + form.image_file.data.filename
        # app.static_folder é o path que o flask olha para onde irá renderizar as imagens na aplicação
        form.image_file.data.save(os.path.join(app.static_folder, image))
        text = form.text.data
    return render_template('topic.html', form=form, image=image, text=text)


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
    return render_template('index.html')


@main.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


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
    return render_template('user.html', user=user)


# @main.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.ping()
#         if not current_user.confirmed and request.endpoint != 'main' and request.blueprint != 'static':
#             return redirect(url_for('main.unconfirmed'))


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
