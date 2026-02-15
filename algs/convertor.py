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

# class RomanToArab:
#     '''
#     Клас конвертор арабські -> римські
#     '''


# if __name__ == '__main__':
#     assert ArabToRoman("1").convert_to_roman() == "I"
#     assert ArabToRoman("4").convert_to_roman() == "IV"
#     assert ArabToRoman("9").convert_to_roman() == "IX"
#     assert ArabToRoman("58").convert_to_roman() == "LVIII"
#     assert ArabToRoman("1994").convert_to_roman() == "MCMXCIV"

#     print("Всі тести пройшли ✅")
