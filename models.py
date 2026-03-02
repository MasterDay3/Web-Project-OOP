# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    level = db.Column(db.Integer, default=1)
    xp = db.Column(db.Integer, default=0)
    daily_goal = db.Column(db.Integer, default=20)
    streak = db.Column(db.Integer, default=0)
    last_active = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # зв'язки
    progress = db.relationship("UserProgress", backref="user", lazy=True)
    attempts = db.relationship("TaskAttempt", backref="user", lazy=True)
    sessions = db.relationship("DailySession", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_xp(self, amount: int):
        """Додає XP і підвищує рівень якщо треба (кожні 100 XP = 1 рівень)."""
        self.xp += amount
        self.level = 1 + self.xp // 100


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(
        db.String(20), nullable=False
    )  # roman / arabic / egyptian / thai / binary
    difficulty = db.Column(db.String(10), nullable=False)  # easy / medium / hard
    question = db.Column(db.String(255), nullable=False)  # текст питання
    correct = db.Column(db.String(100), nullable=False)  # правильна відповідь
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)

    # attempts = db.relationship("TaskAttempt", backref="task", lazy=True)


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    system = db.Column(db.String(20), nullable=False)  # за яку систему прогрес
    tasks_done = db.Column(db.Integer, default=0)
    tasks_correct = db.Column(db.Integer, default=0)

    __table_args__ = (db.UniqueConstraint("user_id", "system"),)

    @property
    def accuracy(self):
        if self.tasks_done == 0:
            return 0
        return round(self.tasks_correct / self.tasks_done * 100, 1)


class TaskAttempt(db.Model):
    __tablename__ = "task_attempts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False)
    system = db.Column(db.String(20), nullable=False)  # ← додай це
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)


class DailySession(db.Model):
    __tablename__ = "daily_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    tasks_done = db.Column(db.Integer, default=0)
    goal_met = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint("user_id", "date"),)
