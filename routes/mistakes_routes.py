# routes/mistakes_routes.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import db, TaskAttempt
from tasks import TaskGenerator
from datetime import datetime

mistakes_routes = Blueprint("mistakes_routes", __name__)
generator = TaskGenerator()


@mistakes_routes.route("/mistakes")
@login_required
def mistakes():
    # Останні 50 неправильних відповідей
    wrong = (
        TaskAttempt.query.filter_by(user_id=current_user.id, is_correct=False)
        .order_by(TaskAttempt.answered_at.desc())
        .limit(50)
        .all()
    )

    return render_template("mistakes.html", mistakes=wrong)


@mistakes_routes.route("/mistakes/retry", methods=["POST"])
@login_required
def retry_mistake():
    """Генерує нову задачу для тієї самої системи."""
    data = request.get_json()
    system = data.get("system", "roman")
    difficulty = data.get("difficulty", "easy")

    from flask import session

    task = generator.generate(system, difficulty)

    session["current_task"] = {
        "answer": task["answer"],
        "system": task["system"],
        "difficulty": task["difficulty"],
    }

    return jsonify(
        {
            "question": task["question"],
            "options": task["options"],
            "system": task["system"],
        }
    )
