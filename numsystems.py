import math
class Convertor:
    '''
    Клас для конвертації чисел між арабськими та римськими.

    Приймає число у вигляді рядка та дозволяє:
        - перевести арабське число в римське
        - перевести римське число в арабське
    '''
    roman_numbers = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    letters = ['M', 'D', 'C', 'L', 'X', 'V', 'I']

    egyptian_numbers = [
        (1000000, '𓀼'), (100000, '𓆐'), (10000, '𓂭'),
        (1000, '𓆼'), (100, '𓍢'), (10, '𓎆'), (1, '𓏺')
    ]
    egypt_hieroglyphs = ['𓀼', '𓆐', '𓂭', '𓆼', '𓍢', '𓎆', '𓏺']

    thai_numbers = [
        ('0', '๐'), ('1', '๑'), ('2', '๒'), ('3', '๓'),('4', '๔'),
        ('5', '๕'), ('6', '๖'), ('7', '๗'), ('8', '๘'), ('9', '๙')
    ]
    thai_hieroglyphs = ['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙', '-', '.', ',']

    def __init__(self, value):
        self.value = value

    def convert_to_roman(self):
        """
        Converts an Arabic number string to a Roman numeral.

        >>> Convertor("1").convert_to_roman()
        'I'
        >>> Convertor("1994").convert_to_roman()
        'MCMXCIV'
        >>> Convertor("4000").convert_to_roman()
        'Число має бути в діапазоні від 1 до 3999'
        >>> Convertor("abc").convert_to_roman()
        'Невірне числове введення.'
        """
        if not str(self.value).isdigit():
            return 'Невірне числове введення.'

        number = int(self.value)

        if not 0 < number < 4000:
            return 'Число має бути в діапазоні від 1 до 3999'

        roman_number = ''

        for value, symbol in self.roman_numbers:
            while number >= value:
                roman_number += symbol
                number -= value

        return roman_number

    def convert_roman_to_arab(self):
        """
        Converts a Roman numeral string to an Arabic number string.

        >>> Convertor("IX").convert_roman_to_arab()
        '9'
        >>> Convertor("mcmxciv").convert_roman_to_arab()
        '1994'
        >>> Convertor("IC").convert_roman_to_arab()
        'Некоректне число'
        >>> Convertor("123").convert_roman_to_arab()
        'Невірне введення, будь ласка введіть римське число латинськими літерами'
        """
        roman_number = str(self.value).upper()
        if not roman_number.isalpha() or not roman_number.isascii():
            return 'Невірне введення, будь ласка введіть римське число латинськими літерами'
        for sym in roman_number:
            if sym not in self.letters:
                return 'Невірне введення'

        for i in range(len(roman_number) - 1):
            curr = roman_number[i]
            nxt = roman_number[i+1]

            v_curr = 0
            for val, s in self.roman_numbers:
                if s == curr:
                    v_curr = val
                    break

            v_nxt = 0
            for val, s in self.roman_numbers:
                if s == nxt:
                    v_nxt = val
                    break

            if v_curr < v_nxt:
                if curr == 'I' and nxt not in ['V', 'X']:
                    return 'Некоректне число'
                if curr == 'X' and nxt not in ['L', 'C']:
                    return 'Некоректне число'
                if curr == 'C' and nxt not in ['D', 'M']:
                    return 'Некоректне число'
                if curr in ['V', 'L', 'D']:
                    return 'Некоректне число'

        arab_number = 0

        for i, char in enumerate(roman_number):
            current_value = 0
            for value, sym in self.roman_numbers:
                if sym == char:
                    current_value = value
                    break

            next_value = 0
            if i + 1 < len(roman_number):
                next_sym = roman_number[i + 1]
                for value, sym in self.roman_numbers:
                    if sym == next_sym:
                        next_value = value
                        break

# Менший перед більшим -> віднімання
# Більший або рівний наступному -> додавання
            if current_value < next_value:
                arab_number -= current_value
            else:
                arab_number += current_value

        return str(arab_number)

    def convert_to_egyptian(self):
        if not self.value.isdigit():
            return 'Невірне введення'
        number = int(self.value)
        if number <= 0 or number >= 10000000:
            return 'Число має бути в діапазоні від 1 до 9999999'

        result = ''
        for value, symbol in self.egyptian_numbers:
            count = number // value
            result += symbol * count
            number %= value

        return result

    def convert_egyptian_to_arab(self):
        number = self.value
        result = 0
        for char in number:
            if char not in self.egypt_hieroglyphs:
                return 'Невірне введення, такого числа немає в єгипетській системі числення'
        for val, sym in self.egyptian_numbers:
            result += number.count(sym) * val
        return str(result)

    def convert_to_thai(self):
        number = self.value.strip()

        if not number:
            return 'Невірне введення'
        if number.count('-') > 1 or (number.count('-') == 1 and number[0] != '-'):
            return 'Невірне введення'
        if number.count('.') + number.count(',') > 1:
            return 'Невірне введення'
        if '.' in number:
            parts = number.split('.')
            if not parts[0].replace('-', '').isdigit() or not parts[1].isdigit():
                return 'Невірне введення'
        elif ',' in number:
            parts = number.split(',')
            if not parts[0].replace('-', '').isdigit() or not parts[1].isdigit():
                return 'Невірне введення'
        else:
            if not number.replace('-', '').isdigit():
                return 'Невірне введення'

        for arabic, thai in self.thai_numbers:
            number = number.replace(arabic, thai)

        return number

    def convert_thai_to_arab(self):
        number = self.value.strip()
        for sym in number:
            if sym not in self.thai_hieroglyphs:
                return 'Невірне введення'

        for arabic, thai in self.thai_numbers:
            number = number.replace(thai, arabic)

        if number.count('-') > 1 or (number.count('-') == 1 and number[0] != '-'):
            return 'Невірне введення'
        if number.count('.') + number.count(',') > 1:
            return 'Невірне введення'

        if '.' in number:
            parts = number.split('.')
            if not parts[0].replace('-', '').isdigit() or not parts[1].isdigit():
                return 'Невірне введення'
        elif ',' in number:
            parts = number.split(',')
            if not parts[0].replace('-', '').isdigit() or not parts[1].isdigit():
                return 'Невірне введення'
        else:
            if not number.replace('-', '').isdigit():
                return 'Невірне введення'

        return number


class Calculator:
    supported_systems = ['arabic', 'roman', 'egyptian', 'thai']
    supported_operations_for_two_nums = ['+', '-', '*', '/', 'power', '%']
    supported_operations_for_one_num = ['!', 'sqrt']
    def __init__(self, number1: str, operation: str, number2: str = None, number_system: str = 'arabic'):
        self.number1 = str(number1).strip()
        self.operation = operation.strip()
        self.number2 = str(number2).strip() if number2 is not None else None
        self.number_system = number_system.lower().strip()

    def calculate(self):
        if self.operation in self.supported_operations_for_two_nums and self.number2 is not None:
            two_nums = True
        elif self.operation in self.supported_operations_for_two_nums and self.number2 is None:
            raise ValueError('Для цієї операції потрібно 2 числа')
        elif self.operation in self.supported_operations_for_one_num and self.number2 is None:
            two_nums = False
        elif self.operation in self.supported_operations_for_one_num and self.number2 is not None:
            raise ValueError('Для цієї операції потрібно лише 1 число')
        else: raise ValueError(f"Непідтримувана операція '{self.operation}'")
        match self.number_system:
            case 'arabic':
                if two_nums:
                    try:
                        a = float(self.number1)
                        b = float(self.number2)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '+':
                            res = a + b
                            if res == int(res):
                                res = int(res)
                        case '-':
                            res = a - b
                            if res == int(res):
                                res = int(res)
                        case '*':
                            res = a * b
                            if res == int(res):
                                res = int(res)
                        case '/':
                            res = a / b
                            if res == int(res):
                                res = int(res)
                        case 'power':
                            res = a ** b
                            if res == int(res):
                                res = int(res)
                        case '%':
                            res = a % b
                            if res == int(res):
                                res = int(res)
                        case _:
                            return 'Такої операції не існує'
                if not two_nums:
                    try:
                        a = float(self.number1)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '!':
                            if a != int(a):
                                raise ValueError("Факторіал визначений лише для невід'ємних цілих чисел")
                            res = math.factorial(int(a))
                            if res == int(res):
                                res = int(res)
                        case 'sqrt':
                            res = math.sqrt(a)
                            if res == int(res):
                                res = int(res)
            case 'roman':
                if two_nums:
                    a = Convertor(self.number1).convert_roman_to_arab()
                    b = Convertor(self.number2).convert_roman_to_arab()
                    try:
                        a = float(a)
                        b = float(b)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '+':
                            result = a + b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case '-':
                            result = a - b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case '*':
                            result = a * b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case '/':
                            result = a / b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case 'power':
                            result = a ** b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case '%':
                            result = a % b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case _:
                            return 'Такої операції не існує'
                if not two_nums:
                    a = Convertor(self.number1).convert_roman_to_arab()
                    try:
                        a = float(a)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '!':
                            if a != int(a):
                                raise ValueError("Факторіал визначений лише для невід'ємних цілих чисел")
                            result = math.factorial(int(a))
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
                        case 'sqrt':
                            result = math.sqrt(a)
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_roman()
            case 'egyptian':
                if two_nums:
                    a = Convertor(self.number1).convert_egyptian_to_arab()
                    b = Convertor(self.number2).convert_egyptian_to_arab()
                    try:
                        a = float(a)
                        b = float(b)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '+':
                            result = a + b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
                        case '-':
                            result = a - b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
                        case '*':
                            result = a * b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
                        case '/':
                            result = a / b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
                        case 'power':
                            result = a ** b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
                        case '%':
                            result = a % b
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
                        case _:
                            return 'Такої операції не існує'
                if not two_nums:
                    a = Convertor(self.number1).convert_egyptian_to_arab()
                    try:
                        a = float(a)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '!':
                            if a != int(a):
                                raise ValueError("Факторіал визначений лише для невід'ємних цілих чисел")
                            result = math.factorial(int(a))
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = res = Convertor(str(result)).convert_to_egyptian()
                        case 'sqrt':
                            result = math.sqrt(a)
                            if result != int(result):
                                raise ValueError('У цій системі числення немає дробових чисел')
                            result = int(result)
                            res = Convertor(str(result)).convert_to_egyptian()
            case 'thai':
                if two_nums:
                    a = Convertor(self.number1).convert_thai_to_arab()
                    b = Convertor(self.number2).convert_thai_to_arab()
                    try:
                        a = float(a)
                        b = float(b)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '+':
                            result = a + b
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
                        case '-':
                            result = a - b
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
                        case '*':
                            result = a * b
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
                        case '/':
                            result = a / b
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
                        case 'power':
                            result = a ** b
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
                        case '%':
                            result = a % b
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
                        case _:
                            return 'Такої операції не існує'
                if not two_nums:
                    a = Convertor(self.number1).convert_thai_to_arab()
                    try:
                        a = float(a)
                    except ValueError as exc:
                        raise ValueError('Некоректне введення') from exc
                    match self.operation:
                        case '!':
                            if a != int(a):
                                raise ValueError("Факторіал визначений лише для невід'ємних цілих чисел")
                            result = math.factorial(int(a))
                            if result == int(result):
                                result = int(result)
                            res = res = Convertor(str(result)).convert_to_thai()
                        case 'sqrt':
                            result = math.sqrt(a)
                            if result == int(result):
                                result = int(result)
                            res = Convertor(str(result)).convert_to_thai()
            case _:
                raise TypeError('Такої системи числення не існує')
        return str(res)

def test():
    print("-" * 30)
    # Тести для convert_to_roman
    assert Convertor("1").convert_to_roman() == "I"
    assert Convertor("4").convert_to_roman() == "IV"
    assert Convertor("9").convert_to_roman() == "IX"
    assert Convertor("49").convert_to_roman() == "XLIX"
    assert Convertor("1994").convert_to_roman() == "MCMXCIV"
    assert Convertor("3999").convert_to_roman() == "MMMCMXCIX"
    assert Convertor("4000").convert_to_roman() == 'Число має бути в діапазоні від 1 до 3999'
    assert Convertor("abc").convert_to_roman() == 'Невірне числове введення.'

    # Тести для convert_roman_to_arab
    assert Convertor("I").convert_roman_to_arab() == "1"
    assert Convertor("IV").convert_roman_to_arab() == "4"
    assert Convertor("IX").convert_roman_to_arab() == "9"
    assert Convertor("XLIX").convert_roman_to_arab() == "49"
    assert Convertor("MCMXCIV").convert_roman_to_arab() == "1994"
    
    assert Convertor("ix").convert_roman_to_arab() == "9"
    assert Convertor("mcmxciv").convert_roman_to_arab() == "1994"
    
    assert Convertor("IC").convert_roman_to_arab() == "Некоректне число"
    assert Convertor("XM").convert_roman_to_arab() == "Некоректне число"
    assert Convertor("VX").convert_roman_to_arab() == "Некоректне число"
    
    assert Convertor("123").convert_roman_to_arab() == "Невірне введення, будь ласка введіть римське число латинськими літерами"
    assert Convertor("ABC").convert_roman_to_arab() == "Невірне введення"

    # Перевірка взаємодії
    test_nums = ["1", "44", "99", "3999"]
    for n in test_nums:
        r = Convertor(n).convert_to_roman()
        a = Convertor(r).convert_roman_to_arab()
        assert n == a

    print("Roman tests done! 🏛️")
    print("-" * 30)

    # --- EGYPTIAN TESTS ---
    # 1. Арабські -> Єгипетські
    assert Convertor("1").convert_to_egyptian() == "𓏺"
    assert Convertor("10").convert_to_egyptian() == "𓎆"
    assert Convertor("12").convert_to_egyptian() == "𓎆𓏺𓏺"
    assert Convertor("4622").convert_to_egyptian() == "𓆼𓆼𓆼𓆼𓍢𓍢𓍢𓍢𓍢𓍢𓎆𓎆𓏺𓏺"

    error_range = 'Число має бути в діапазоні від 1 до 9999999'
    assert Convertor("0").convert_to_egyptian() == error_range
    assert Convertor("10000000").convert_to_egyptian() == error_range

    # 2. Єгипетські -> Арабські
    assert Convertor("𓏺").convert_egyptian_to_arab() == "1"
    assert Convertor("𓎆").convert_egyptian_to_arab() == "10"
    assert Convertor("𓎆𓏺𓏺").convert_egyptian_to_arab() == "12"
    assert Convertor("𓏺𓎆𓏺").convert_egyptian_to_arab() == "12"

    error_invalid = 'Невірне введення, такого числа немає в єгипетській системі числення'
    assert Convertor("ABC").convert_egyptian_to_arab() == error_invalid
    assert Convertor("123").convert_egyptian_to_arab() == error_invalid

    test_val = "1234"
    egyptian_str = Convertor(test_val).convert_to_egyptian()
    arabic_res = Convertor(egyptian_str).convert_egyptian_to_arab()
    assert test_val == arabic_res

    print("Egyptian tests done! 𓆼 ✅")
    print("-" * 30)

    # 1. Арабські -> Тайські
    assert Convertor("1").convert_to_thai() == "๑"
    assert Convertor("10").convert_to_thai() == "๑๐"
    assert Convertor("2024").convert_to_thai() == "๒๐๒๔"
    assert Convertor("-123").convert_to_thai() == "-๑๒๓"
    assert Convertor("12.5").convert_to_thai() == "๑๒.๕"
    assert Convertor("12,5").convert_to_thai() == "๑๒,๕"
    assert Convertor("34567").convert_to_thai() == "๓๔๕๖๗"
    assert Convertor("12.5,6").convert_to_thai() == 'Невірне введення'
    assert Convertor("--123").convert_to_thai() == 'Невірне введення'
    assert Convertor("123-").convert_to_thai() == 'Невірне введення'
    assert Convertor("12a").convert_to_thai() == 'Невірне введення'
    assert Convertor("12..5").convert_to_thai() == 'Невірне введення'

    # --- Тайські -> Арабські ---
    assert Convertor("๑").convert_thai_to_arab() == "1"
    assert Convertor("๑๐").convert_thai_to_arab() == "10"
    assert Convertor("๒๐๒๔").convert_thai_to_arab() == "2024"
    assert Convertor("๓๔๕๖๗").convert_thai_to_arab() == "34567"
    assert Convertor("-๑๒๓").convert_thai_to_arab() == "-123"
    assert Convertor("๑๒.๕").convert_thai_to_arab() == "12.5"
    assert Convertor("๑๒,๕").convert_thai_to_arab() == "12,5"
    assert Convertor("๑๒.๕,๖").convert_thai_to_arab() == "Невірне введення"
    assert Convertor("--๑๒๓").convert_thai_to_arab() == "Невірне введення"
    assert Convertor("๑๒A").convert_thai_to_arab() == "Невірне введення"
    assert Convertor("๑๒๓-").convert_thai_to_arab() == "Невірне введення"

    # --- Round-trip tests ---
    test_vals = ["34567", "-456", "12.75", "12,5"]
    for val in test_vals:
        thai_str = Convertor(val).convert_to_thai()
        arabic_res = Convertor(thai_str).convert_thai_to_arab()
        assert val == arabic_res

    print("Thai tests done! 🇹🇭 ✅")
    print("-" * 30)
    # Передбачається що Convertor і Calculator вже імпортовані

    # ── ARABIC ──
    assert Calculator('10', '+', '5').calculate() == '15'
    assert Calculator('10', '-', '3').calculate() == '7'
    assert Calculator('4',  '*', '3').calculate() == '12'
    assert Calculator('10', '/', '2').calculate() == '5'
    assert Calculator('2',  'power', '8').calculate() == '256'
    assert Calculator('10', '%', '3').calculate() == '1'
    assert Calculator('5',  '!').calculate() == '120'
    assert Calculator('0',  '!').calculate() == '1'
    assert Calculator('9',  'sqrt').calculate() == '3'
    # дробові — залишаються
    assert Calculator('1',  '/', '4').calculate() == '0.25'
    assert Calculator('2.5', '+', '1.5').calculate() == '4'
    assert Calculator('-5', '+', '3').calculate() == '-2'
    try: Calculator('10', '+').calculate(); assert False
    except ValueError: pass
    try: Calculator('5', '!', '3').calculate(); assert False
    except ValueError: pass
    try: Calculator('abc', '+', '2').calculate(); assert False
    except ValueError: pass
    try: Calculator('5', '/', '0').calculate(); assert False
    except ZeroDivisionError: pass
    try: Calculator('5', '??').calculate(); assert False
    except ValueError: pass
    try: Calculator('2.5', '!').calculate(); assert False
    except ValueError: pass
    print('ARABIC: OK')

    # ── ROMAN ──
    assert Calculator('X',  '+',     'V',    'roman').calculate() == 'XV'
    assert Calculator('X',  '-',     'V',    'roman').calculate() == 'V'
    assert Calculator('V',  '*',     'III',  'roman').calculate() == 'XV'
    assert Calculator('X',  '/',     'II',   'roman').calculate() == 'V'
    assert Calculator('II', 'power', 'VIII', 'roman').calculate() == 'CCLVI'
    assert Calculator('X',  '%',     'III',  'roman').calculate() == 'I'
    assert Calculator('III','!', number_system='roman').calculate() == 'VI'
    assert Calculator('IV', 'sqrt', number_system='roman').calculate() == 'II'
    # дробовий результат -> ValueError
    try: Calculator('X', '/', 'III', 'roman').calculate(); assert False
    except ValueError: pass
    # від'ємний результат -> Convertor поверне рядок помилки (не ValueError)
    assert Calculator('I', '-', 'V', 'roman').calculate() == 'Невірне числове введення.'
    # невалідний ввід
    try: Calculator('123', '+', 'V', 'roman').calculate(); assert False
    except ValueError: pass
    print('ROMAN: OK')

    # ── EGYPTIAN ──
    assert Calculator('𓎆𓎆', '+', '𓎆𓎆𓎆', 'egyptian').calculate() == '𓎆𓎆𓎆𓎆𓎆'  # 20+30=50
    assert Calculator('𓎆',   '*', '𓎆',     'egyptian').calculate() == '𓍢'         # 10*10=100
    assert Calculator('𓍢',   '-', '𓎆',     'egyptian').calculate() == '𓎆𓎆𓎆𓎆𓎆𓎆𓎆𓎆𓎆'  # 100-10=90 (9 tens)
    assert Calculator('𓎆𓎆',  '/', '𓎆',     'egyptian').calculate() == '𓏺𓏺'        # 20/10=2
    assert Calculator('𓎆',   '!', number_system='egyptian').calculate() == '𓀼𓀼𓀼𓆐𓆐𓆐𓆐𓆐𓆐𓂭𓂭𓆼𓆼𓆼𓆼𓆼𓆼𓆼𓆼𓍢𓍢𓍢𓍢𓍢𓍢𓍢𓍢'  # 10!=3628800
    assert Calculator('𓍢',   'sqrt', number_system='egyptian').calculate() == '𓎆'  # sqrt(100)=10
    # дробовий результат
    try: Calculator('𓎆', '/', '𓎆𓎆𓎆', 'egyptian').calculate(); assert False  # 10/30
    except ValueError: pass
    print('EGYPTIAN: OK')

    # ── THAI ──
    assert Calculator('๑๐', '+', '๕',  'thai').calculate() == '๑๕.๐'   # 10+5=15
    assert Calculator('๙',  '*', '๙',  'thai').calculate() == '๘๑.๐'    # 9*9=81
    assert Calculator('๑๐', '-', '๓',  'thai').calculate() == '๗.๐'   # 10-3=7
    assert Calculator('๔',  '!', number_system='thai').calculate() == '๒๔'   # 4!=24
    assert Calculator('๙',  'sqrt', number_system='thai').calculate() == '๓.๐'  # sqrt(9)=3.0
    assert Calculator('๑',  '/', '๔',  'thai').calculate() == '๐.๒๕'  # 1/4=0.25 (thai підтримує дроби)
    print('THAI: OK')

    print('\nВсі тести пройшл')

if __name__ == '__main__':
    #test()
    pass
