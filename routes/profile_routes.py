# routes/profile_routes.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User

profile_routes = Blueprint("profile_routes", __name__)


@profile_routes.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "update_info":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()

            if not username or not email:
                flash("Імʼя та email не можуть бути порожніми", "error")
                return redirect(url_for("profile_routes.profile"))

            # перевірка унікальності
            if username != current_user.username:
                if User.query.filter_by(username=username).first():
                    flash("Це імʼя вже зайняте", "error")
                    return redirect(url_for("profile_routes.profile"))

            if email != current_user.email:
                if User.query.filter_by(email=email).first():
                    flash("Цей email вже використовується", "error")
                    return redirect(url_for("profile_routes.profile"))

            current_user.username = username
            current_user.email = email
            db.session.commit()
            flash("Профіль оновлено!", "success")

        elif action == "update_password":
            old_password = request.form.get("old_password", "")
            new_password = request.form.get("new_password", "")
            confirm = request.form.get("confirm_password", "")

            if not current_user.check_password(old_password):
                flash("Старий пароль невірний", "error")
                return redirect(url_for("profile_routes.profile"))

            if len(new_password) < 6:
                flash("Новий пароль має бути мінімум 6 символів", "error")
                return redirect(url_for("profile_routes.profile"))

            if new_password != confirm:
                flash("Паролі не співпадають", "error")
                return redirect(url_for("profile_routes.profile"))

            current_user.set_password(new_password)
            db.session.commit()
            flash("Пароль змінено!", "success")

        elif action == "update_goal":
            try:
                goal = int(request.form.get("daily_goal", 20))
                if not 1 <= goal <= 200:
                    raise ValueError
            except ValueError:
                flash("Денна ціль має бути від 1 до 200", "error")
                return redirect(url_for("profile_routes.profile"))

            current_user.daily_goal = goal
            db.session.commit()
            flash("Денну ціль оновлено!", "success")

        return redirect(url_for("profile_routes.profile"))

    return render_template("profile.html")
