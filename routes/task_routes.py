# routes/task_routes.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, render_template, request, jsonify, session
from flask_login import login_required, current_user
from models import db, TaskAttempt, UserProgress, DailySession
from tasks import TaskGenerator
from datetime import date

task_routes = Blueprint("task_routes", __name__)
generator = TaskGenerator()


@task_routes.route("/tasks")
@login_required
def tasks_page():
    return render_template("tasks.html")


@task_routes.route("/tasks/generate", methods=["POST"])
@login_required
def generate_task():
    data = request.get_json()
    system = data.get("system", "roman")
    difficulty = data.get("difficulty", "easy")

    task = generator.generate(system, difficulty)

    # зберігаємо правильну відповідь в сесії (щоб не слати на фронт)
    session["current_task"] = {
        "answer": task["answer"],
        "system": task["system"],
        "difficulty": task["difficulty"],
    }

    # на фронт відповідь НЕ відправляємо
    return jsonify(
        {
            "question": task["question"],
            "options": task["options"],
            "system": task["system"],
        }
    )


@task_routes.route("/tasks/answer", methods=["POST"])
@login_required
def submit_answer():
    data = request.get_json()
    user_answer = data.get("answer", "").strip()

    current = session.get("current_task")
    if not current:
        return jsonify({"error": "Немає активної задачі"}), 400

    correct = current["answer"]
    system = current["system"]
    difficulty = current["difficulty"]
    is_correct = user_answer == correct

    # ── 1. Зберігаємо спробу ──────────────────────────────────────────────
    attempt = TaskAttempt(
        user_id=current_user.id,
        is_correct=is_correct,
        system=system,
    )
    db.session.add(attempt)

    # ── 2. Оновлюємо прогрес по системі ──────────────────────────────────
    progress = UserProgress.query.filter_by(
        user_id=current_user.id, system=system
    ).first()

    if not progress:
        progress = UserProgress(user_id=current_user.id, system=system)
        db.session.add(progress)
        db.session.flush()

    progress.tasks_done += 1

    if is_correct:
        progress.tasks_correct += 1

    # ── 3. XP і рівень ───────────────────────────────────────────────────
    xp_gained = 0
    if is_correct:
        xp_gained = {"easy": 5, "medium": 10, "hard": 20}[difficulty]
        current_user.add_xp(xp_gained)

    # ── 4. Денна сесія і стрік ────────────────────────────────────────────
    today = date.today()
    daily = DailySession.query.filter_by(user_id=current_user.id, date=today).first()

    if not daily:
        daily = DailySession(user_id=current_user.id, date=today)
        db.session.add(daily)
        db.session.flush()

    daily.tasks_done += 1
    if daily.tasks_done >= current_user.daily_goal:
        daily.goal_met = True
        # оновлюємо стрік
        current_user.streak += 1

    current_user.last_active = today
    db.session.commit()

    return jsonify(
        {
            "is_correct": is_correct,
            "correct": correct,
            "xp_gained": xp_gained,
            "total_xp": current_user.xp,
            "level": current_user.level,
            "streak": current_user.streak,
            "tasks_today": daily.tasks_done,
            "goal": current_user.daily_goal,
            "goal_met": daily.goal_met,
        }
    )
