class Convertor:
    '''
    Клас для конвертації чисел між арабськими та римськими.

    Приймає число у вигляді рядка та дозволяє:
        - перевести арабське число в римське
        - перевести римське число в арабське
    '''
    numbers = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    letters = ['M', 'D', 'C', 'L', 'X', 'V', 'I']

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
        'Number must be in range from 1 to 3999'
        >>> Convertor("abc").convert_to_roman()
        'Invalid number input.'
        """
        if not str(self.value).isdigit():
            return 'Invalid number input.'

        number = int(self.value)

        if not 0 < number < 4000:
            return 'Number must be in range from 1 to 3999'

        roman_number = ''

        for value, symbol in self.numbers:
            while number >= value:
                roman_number += symbol
                number -= value

        return roman_number

    def convert_to_arab(self):
        """
        Converts a Roman numeral string to an Arabic number string.

        >>> Convertor("IX").convert_to_arab()
        '9'
        >>> Convertor("mcmxciv").convert_to_arab()
        '1994'
        >>> Convertor("IC").convert_to_arab()
        'Incorrect number entered'
        >>> Convertor("123").convert_to_arab()
        'Invalid input, please enter a Roman numeral using Latin letters'
        """
        roman_number = str(self.value).upper()
        if not roman_number.isalpha() or not roman_number.isascii():
            return 'Invalid input, please enter a Roman numeral using Latin letters'
        for sym in roman_number:
            if sym not in self.letters:
                return 'Invalid input'

        for i in range(len(roman_number) - 1):
            curr = roman_number[i]
            nxt = roman_number[i+1]

            v_curr = 0
            for val, s in self.numbers:
                if s == curr:
                    v_curr = val
                    break

            v_nxt = 0
            for val, s in self.numbers:
                if s == nxt:
                    v_nxt = val
                    break

            if v_curr < v_nxt:
                if curr == 'I' and nxt not in ['V', 'X']:
                    return 'Incorrect number entered'
                if curr == 'X' and nxt not in ['L', 'C']:
                    return 'Incorrect number entered'
                if curr == 'C' and nxt not in ['D', 'M']:
                    return 'Incorrect number entered'
                if curr in ['V', 'L', 'D']:
                    return 'Incorrect number entered'

        arab_number = 0

        for i, char in enumerate(roman_number):
            current_value = 0
            for value, sym in self.numbers:
                if sym == char:
                    current_value = value
                    break

            next_value = 0
            if i + 1 < len(roman_number):
                next_sym = roman_number[i + 1]
                for value, sym in self.numbers:
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


if __name__ == '__main__':
    # Тести для convert_to_roman
    assert Convertor("1").convert_to_roman() == "I"
    assert Convertor("4").convert_to_roman() == "IV"
    assert Convertor("9").convert_to_roman() == "IX"
    assert Convertor("49").convert_to_roman() == "XLIX"
    assert Convertor("1994").convert_to_roman() == "MCMXCIV"
    assert Convertor("3999").convert_to_roman() == "MMMCMXCIX"
    assert Convertor("4000").convert_to_roman() == 'Number must be in range from 1 to 3999'
    assert Convertor("abc").convert_to_roman() == 'Invalid number input.'

    # Тести для convert_to_arab
    assert Convertor("I").convert_to_arab() == "1"
    assert Convertor("IV").convert_to_arab() == "4"
    assert Convertor("IX").convert_to_arab() == "9"
    assert Convertor("XLIX").convert_to_arab() == "49"
    assert Convertor("MCMXCIV").convert_to_arab() == "1994"
    
    assert Convertor("ix").convert_to_arab() == "9"
    assert Convertor("mcmxciv").convert_to_arab() == "1994"
    
    assert Convertor("IC").convert_to_arab() == "Incorrect number entered"
    assert Convertor("XM").convert_to_arab() == "Incorrect number entered"
    assert Convertor("VX").convert_to_arab() == "Incorrect number entered"
    
    assert Convertor("123").convert_to_arab() == "Invalid input, please enter a Roman numeral using Latin letters"
    assert Convertor("ABC").convert_to_arab() == "Invalid input"

    # Перевірка взаємодії
    test_nums = ["1", "44", "99", "3999"]
    for n in test_nums:
        r = Convertor(n).convert_to_roman()
        a = Convertor(r).convert_to_arab()
        assert n == a

    print("All tests passed! ✅")
