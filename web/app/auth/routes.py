from flask_login import current_user, login_user, logout_user
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from app.auth.forms import RegistrationForm, LoginForm
from app.auth import bp
from app.models import User
from app import db

@bp.route("/register", methods=['post', 'get'])
def register():
    form = RegistrationForm()
    
    # Upon submission
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if not existing_user and form.nickname.data and form.email.data:
            user = User(nickname=form.nickname.data, 
                        email=form.email.data,
                        consent_to_send_emails= request.form.get('add_word__news'), 
                        consent_to_cookies=request.form.get('add_word__cookie'))
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        
            flash(f'Жаны автор {form.nickname.data} кошулду!')
            return redirect(url_for('main.index'))
        else:
            flash('Бул имейл менен автор катталган!', 'error')

    return render_template('user_registration.html', title='Registration', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if not existing_user or not existing_user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))

        login_user(existing_user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))

    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))