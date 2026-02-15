class ArabToRoman:
    '''
    Клас конвертор арабські -> римські
    '''
    roman_numbers = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]

    def __init__(self, number):
        self.number = number

    def convert_to_roman(self):
        '''
        Функція, яка конвертує арабські числа в римські
        '''
        if not self.number.isdigit():
            return 'Неправильний ввід числа.'

        number = int(self.number)

        if not 0 < number < 4000:
            return 'Число повинне бути в проміжку від 1 до 3999'

        roman_number = ''

        for value, symbol in self.roman_numbers:
            while number >= value:
                roman_number += symbol
                number -= value

        return roman_number

class RomanToArab:
    '''
    Клас конвертор арабські -> римські
    '''
    arab_numbers = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    letters = ['M','D','C','L','X','V','I']

    def __init__(self, roman_number):
        self.roman_number = roman_number

    def convert_to_arab(self):
        '''
        Функція, яка конвертує римські числа в арабські
        '''
        roman_number = self.roman_number
        if not roman_number.isalpha() or not roman_number.isascii():
            return 'Не правильний ввід, введіть число латинецею'
        for sym in roman_number:
            if sym.upper() not in self.letters:
                return 'Не правильний ввід'

        arab_number = 0

        for i, char in enumerate(roman_number):
            current_value = 0
            for value, sym in self.arab_numbers:
                if sym == char:
                    current_value = value
                    break

            next_value = 0
            if i + 1 < len(roman_number):
                next_sym = roman_number[i + 1]
                for value, sym in self.arab_numbers:
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
