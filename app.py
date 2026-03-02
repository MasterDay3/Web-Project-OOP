import os
from flask import Flask, render_template, request
from models import db, User
from flask_login import LoginManager, login_required, current_user
from routes.auth_routes import auth_routes
from numsystems import Convertor, Calculator
from flask_migrate import Migrate
from routes.task_routes import task_routes
from routes.leaderboard_routes import leaderboard_routes
from routes.profile_routes import profile_routes
from routes.stats_routes import stats_routes
from routes.mistakes_routes import mistakes_routes

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev_secret_key_change_in_prod")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///users.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.register_blueprint(profile_routes)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_routes.login"
app.register_blueprint(stats_routes)
app.register_blueprint(mistakes_routes)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# підключаємо маршрути
auth_routes.name = "auth_routes"
app.register_blueprint(auth_routes)
app.register_blueprint(task_routes)
app.register_blueprint(leaderboard_routes)


def eval_calc_expression(expr: str, system: str):
    """Обчислює вираз з дужками і кількома операторами у заданій системі числення.
    Повертає (result_str, error_str) — одне з двох буде None."""
    if not expr or not expr.strip():
        return None, "Не вдалося розібрати вираз"

    s = expr.strip().replace(" ", "")

    digit_chars = {
        "roman": set("MDCLXVImdclxvi"),
        "arabic": set("0123456789."),
        "egyptian": set("𓀼𓆐𓂭𓆼𓍢𓎆𓏺"),
        "thai": set("๐๑๒๓๔๕๖๗๘๙."),
    }
    digits = digit_chars.get(system, digit_chars["arabic"])
    ops = {"+", "-", "×", "÷"}

    # ── Токенізація ──
    tokens = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in digits:
            j = i
            while j < len(s) and s[j] in digits:
                j += 1
            tokens.append(("NUM", s[i:j]))
            i = j
        elif ch in ops:
            tokens.append(("OP", ch))
            i += 1
        elif ch == "(":
            tokens.append(("LPAREN", "("))
            i += 1
        elif ch == ")":
            tokens.append(("RPAREN", ")"))
            i += 1
        else:
            return None, f"Невідомий символ: {ch}"

    if not tokens:
        return None, "Не вдалося розібрати вираз"

    # ── Конвертація числового токена в float ──
    def to_arabic(num_str):
        if system == "roman":
            r = Convertor(num_str).convert_roman_to_arab()
        elif system == "egyptian":
            r = Convertor(num_str).convert_egyptian_to_arab()
        elif system == "thai":
            r = Convertor(num_str).convert_thai_to_arab()
        else:
            r = num_str
        return float(r)

    # ── Shunting-yard ──
    precedence = {"+": 1, "-": 1, "×": 2, "÷": 2}
    output = []
    op_stack = []

    for tok_type, tok_val in tokens:
        if tok_type == "NUM":
            try:
                output.append(to_arabic(tok_val))
            except (ValueError, TypeError):
                return None, f"Невірне число: {tok_val}"
        elif tok_type == "OP":
            while (
                op_stack
                and op_stack[-1] != "("
                and precedence.get(op_stack[-1], 0) >= precedence.get(tok_val, 0)
            ):
                output.append(op_stack.pop())
            op_stack.append(tok_val)
        elif tok_type == "LPAREN":
            op_stack.append("(")
        elif tok_type == "RPAREN":
            while op_stack and op_stack[-1] != "(":
                output.append(op_stack.pop())
            if not op_stack:
                return None, "Незбалансовані дужки"
            op_stack.pop()

    while op_stack:
        if op_stack[-1] == "(":
            return None, "Незбалансовані дужки"
        output.append(op_stack.pop())

    # ── Обчислення RPN ──
    stack = []
    for item in output:
        if isinstance(item, float):
            stack.append(item)
        else:
            if len(stack) < 2:
                return None, "Не вдалося розібрати вираз"
            b, a = stack.pop(), stack.pop()
            if item == "+":
                stack.append(a + b)
            elif item == "-":
                stack.append(a - b)
            elif item == "×":
                stack.append(a * b)
            elif item == "÷":
                if b == 0:
                    return None, "Ділення на нуль"
                stack.append(a / b)

    if len(stack) != 1:
        return None, "Не вдалося розібрати вираз"

    result = stack[0]
    if isinstance(result, float) and result == int(result):
        result = int(result)

    # ── Конвертація результату назад ──
    if system == "arabic":
        return str(result), None
    if system in ("roman", "egyptian"):
        if isinstance(result, float) and result != int(result):
            return None, "У цій системі немає дробових чисел"
        result = int(result)
    if system == "roman":
        return str(Convertor(str(result)).convert_to_roman()), None
    if system == "egyptian":
        return str(Convertor(str(result)).convert_to_egyptian()), None
    if system == "thai":
        return str(Convertor(str(result)).convert_to_thai()), None
    return str(result), None


@app.route("/dashboard")
@login_required
def dashboard():
    from models import UserProgress, DailySession, TaskAttempt
    from datetime import date, timedelta

    # Прогрес по системах
    progress = UserProgress.query.filter_by(user_id=current_user.id).all()

    # Денна сесія
    today = date.today()
    daily = DailySession.query.filter_by(user_id=current_user.id, date=today).first()
    tasks_today = daily.tasks_done if daily else 0

    # Останні 7 днів для графіка
    week = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        s = DailySession.query.filter_by(user_id=current_user.id, date=d).first()
        week.append(
            {
                "date": d.strftime("%d.%m"),
                "done": s.tasks_done if s else 0,
                "met": s.goal_met if s else False,
            }
        )

    # Загальна статистика
    total_attempts = TaskAttempt.query.filter_by(user_id=current_user.id).count()
    correct = TaskAttempt.query.filter_by(
        user_id=current_user.id, is_correct=True
    ).count()
    accuracy = round(correct / total_attempts * 100) if total_attempts else 0

    return render_template(
        "dashboard.html",
        progress=progress,
        tasks_today=tasks_today,
        week=week,
        total_attempts=total_attempts,
        accuracy=accuracy,
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/convert", methods=["POST"])
def api_convert():
    from flask import jsonify
    data = request.get_json()
    value = data.get("value", "")
    system_from = data.get("system_from", "")
    system_to = data.get("system_to", "")
    try:
        conv = Convertor(value)

        # Direct conversions from/to Arabic
        to_arabic = {
            "roman":    lambda c: c.convert_roman_to_arab(),
            "egyptian": lambda c: c.convert_egyptian_to_arab(),
            "thai":     lambda c: c.convert_thai_to_arab(),
        }
        from_arabic = {
            "roman":    lambda c: c.convert_to_roman(),
            "egyptian": lambda c: c.convert_to_egyptian(),
            "thai":     lambda c: c.convert_to_thai(),
        }

        if system_from == system_to:
            result = value
        elif system_from == "arabic":
            result = from_arabic[system_to](conv)
        elif system_to == "arabic":
            result = to_arabic[system_from](conv)
        else:
            # Cross-system: chain through Arabic
            arabic_val = str(to_arabic[system_from](conv))
            result = from_arabic[system_to](Convertor(arabic_val))

        result_str = str(result)
        # Convertor methods return Ukrainian error strings instead of raising
        import re
        if re.search(r'[а-яА-ЯіІїЇєЄґҐ]', result_str):
            return jsonify({"result": None, "error": result_str})
        return jsonify({"result": result_str, "error": None})
    except Exception as e:
        return jsonify({"result": None, "error": str(e)})


@app.route("/calculate", methods=["POST"])
def calculate():
    number1 = request.form.get("number1")
    number2 = request.form.get("number2")
    operation = request.form.get("operation")
    system = request.form.get("system")
    try:
        calc = Calculator(number1, operation, number2, system)
        result = calc.calculate()
    except Exception as e:
        result = f"Помилка: {e}"
    return render_template(
        "index.html",
        calc_result=result,
        number1=number1,
        number2=number2,
        operation=operation,
        system=system,
    )


@app.route("/calculator", methods=["GET", "POST"])
def calculator_page():
    expr = ""
    system = "roman"
    calc_result = None
    calc_error = None
    if request.method == "POST":
        expr = request.form.get("expr", "")
        system = request.form.get("system", "roman")
        try:
            calc_result, calc_error = eval_calc_expression(expr, system)
        except Exception as e:
            calc_error = f"Помилка: {e}"
    return render_template(
        "calculator.html",
        expr=expr,
        calc_result=calc_result,
        calc_error=calc_error,
        system=system,
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
