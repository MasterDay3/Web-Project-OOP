from flask import Flask, render_template, request
from models import db, User
from flask_login import LoginManager
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

# Підключаємо маршрути
app.register_blueprint(auth_routes)

# Тимчасовий dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
def home():
    """
    Головна сторінка сайту.
    Тут користувач може обрати систему числення і ввести числа для конвертації або обчислень.
    """
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """
    Обробка конвертації чисел між системами.
    Очікує:
        form fields: value, system_from, system_to
    """
    value = request.form.get('value')
    system_from = request.form.get('system_from')
    system_to = request.form.get('system_to')

    try:
        # Використовуємо Convertor з numsystems.py
        conv = Convertor(value)
        match (system_from, system_to):
            case ('arabic', 'roman'):
                result = conv.convert_to_roman()
            case ('roman', 'arabic'):
                result = conv.convert_roman_to_arab()
            case ('arabic', 'egyptian'):
                result = conv.convert_to_egyptian()
            case ('egyptian', 'arabic'):
                result = conv.convert_egyptian_to_arab()
            case ('arabic', 'thai'):
                result = conv.convert_to_thai()
            case ('thai', 'arabic'):
                result = conv.convert_thai_to_arab()
            case _:
                result = "Ця комбінація конвертації ще не реалізована"
    except Exception as e:
        result = f"Помилка: {str(e)}"

    return render_template('index.html', result=result, value=value, system_from=system_from, system_to=system_to)

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Обробка калькуляцій.
    Очікує:
        form fields: number1, operation, number2, system
    """
    number1 = request.form.get('number1')
    number2 = request.form.get('number2')
    operation = request.form.get('operation')
    system = request.form.get('system')

    try:
        calc = Calculator(number1, operation, number2, system)
        result = calc.calculate()
    except Exception as e:
        result = f"Помилка: {str(e)}"

    return render_template('index.html', calc_result=result, number1=number1,
                           number2=number2, operation=operation, system=system)
 
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)