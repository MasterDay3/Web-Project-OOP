# routes/leaderboard_routes.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, render_template
from flask_login import login_required
from models import db, User

leaderboard_routes = Blueprint("leaderboard_routes", __name__)


@leaderboard_routes.route("/leaderboard")
@login_required
def leaderboard():
    # Топ по XP
    by_xp = User.query.order_by(User.xp.desc()).limit(50).all()

    # Топ по стріку
    by_streak = User.query.order_by(User.streak.desc()).limit(50).all()

    return render_template("leaderboard.html", by_xp=by_xp, by_streak=by_streak)
