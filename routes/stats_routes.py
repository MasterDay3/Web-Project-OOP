# routes/stats_routes.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from models import db, TaskAttempt, UserProgress, DailySession
from datetime import date, timedelta
from sqlalchemy import func

stats_routes = Blueprint("stats_routes", __name__)


@stats_routes.route("/stats")
@login_required
def stats():
    return render_template("stats.html")


@stats_routes.route("/stats/data")
@login_required
def stats_data():
    today = date.today()

    # ── 30 днів активності ────────────────────────────────────────────
    days_labels = []
    tasks_per_day = []
    accuracy_per_day = []

    for i in range(29, -1, -1):
        d = today - timedelta(days=i)
        days_labels.append(d.strftime("%d.%m"))

        session = DailySession.query.filter_by(user_id=current_user.id, date=d).first()
        tasks_per_day.append(session.tasks_done if session else 0)

        # точність за день
        attempts = TaskAttempt.query.filter(
            TaskAttempt.user_id == current_user.id,
            func.date(TaskAttempt.answered_at) == d,
        ).all()

        if attempts:
            correct = sum(1 for a in attempts if a.is_correct)
            accuracy_per_day.append(round(correct / len(attempts) * 100))
        else:
            accuracy_per_day.append(None)

    # ── Успішність по системах ────────────────────────────────────────
    progress = UserProgress.query.filter_by(user_id=current_user.id).all()
    systems_labels = [p.system.capitalize() for p in progress]
    systems_accuracy = [p.accuracy for p in progress]
    systems_done = [p.tasks_done for p in progress]

    return jsonify(
        {
            "days": days_labels,
            "tasks_per_day": tasks_per_day,
            "accuracy_per_day": accuracy_per_day,
            "systems_labels": systems_labels,
            "systems_accuracy": systems_accuracy,
            "systems_done": systems_done,
        }
    )
