# routes/auth_routes.py
import sys
import os

# Додаємо корінь проекту у шляхи Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import db, User
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email вже використовується!')
            return redirect(url_for('auth_routes.register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Реєстрація успішна!')
        return redirect(url_for('auth_routes.login'))

    return render_template('register.html')


@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Успішний вхід!')
            return redirect(url_for('dashboard'))  # Пізніше створимо dashboard
        else:
            flash('Невірний email або пароль!')
    return render_template('login.html')


@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з акаунта')
    return redirect(url_for('auth_routes.login'))