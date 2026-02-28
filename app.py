from flask import Flask, render_template, request
from models import db, User
from flask_login import LoginManager, login_required
from routes.auth_routes import auth_routes
from numsystems import Convertor, Calculator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_routes.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# підключаємо маршрути
auth_routes.name = 'auth_routes'
app.register_blueprint(auth_routes)


def parse_calc_expression(expr: str):
    # Парсер простих виразів для римського калькулятора
    if not expr:
        return None
    s = expr.strip().replace(' ', '')
    if not s:
        return None
    if s.endswith('!'):
        return s[:-1], '!', None
    if s.startswith('√'):
        return s[1:], 'sqrt', None
    if s.lower().startswith('sqrt'):
        return s[4:], 'sqrt', None
    ops_map = {'+':'+','-':'-','*':'*','x':'*','×':'*','/':'/','÷':'/','%':'%','^':'power'}
    for i,ch in enumerate(s):
        if ch in ops_map:
            left, right = s[:i], s[i+1:]
            if left and right:
                return left, ops_map[ch], right
    return None


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert():
    value = request.form.get('value')
    system_from = request.form.get('system_from')
    system_to = request.form.get('system_to')
    try:
        conv = Convertor(value)
        match (system_from, system_to):
            case ('arabic','roman'):
                result = conv.convert_to_roman()
            case ('roman','arabic'):
                result = conv.convert_roman_to_arab()
            case ('arabic','egyptian'):
                result = conv.convert_to_egyptian()
            case ('egyptian','arabic'):
                result = conv.convert_egyptian_to_arab()
            case ('arabic','thai'):
                result = conv.convert_to_thai()
            case ('thai','arabic'):
                result = conv.convert_thai_to_arab()
            case _:
                result = "Ця комбінація конвертації ще не реалізована"
    except Exception as e:
        result = f"Помилка: {e}"
    return render_template('index.html', result=result, value=value,
                           system_from=system_from, system_to=system_to)


@app.route('/calculate', methods=['POST'])
def calculate():
    number1   = request.form.get('number1')
    number2   = request.form.get('number2')
    operation = request.form.get('operation')
    system    = request.form.get('system')
    try:
        calc = Calculator(number1, operation, number2, system)
        result = calc.calculate()
    except Exception as e:
        result = f"Помилка: {e}"
    return render_template('index.html', calc_result=result, number1=number1,
                           number2=number2, operation=operation, system=system)


@app.route('/calculator', methods=['GET','POST'])
def calculator_page():
    expr = ''
    system = 'roman'
    calc_result = None
    calc_error = None
    if request.method == 'POST':
        expr = request.form.get('expr','')
        system = request.form.get('system','roman')
        parsed = parse_calc_expression(expr)
        if not parsed:
            calc_error = 'Не вдалося розібрати вираз'
        else:
            n1, op, n2 = parsed
            try:
                calc = Calculator(n1, op, n2, system)
                calc_result = calc.calculate()
            except Exception as e:
                calc_error = f"Помилка: {e}"
    return render_template('calculator.html', expr=expr,
                           calc_result=calc_result, calc_error=calc_error,
                           system=system)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
