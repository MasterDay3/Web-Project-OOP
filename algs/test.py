class Baryga:
    def __init__(self, r1, r5, next_radix):
        self.symbol1 = r1
        self.symbol5 = r5
        self.higher = next_radix
        self.all_digits = {}
        try:
            for a in range(1, 10):
                self.all_digits[self.arabic2roman(a)] = a
        except Exception:
            pass

    def arabic2roman(self, arabic_digit: int) -> str:
        if arabic_digit > 9:
            raise Exception('Too big digit')
        elif arabic_digit == 9:
            if self.higher is None:
                raise Exception('Unsupported 9')
            return self.symbol1 + self.higher.symbol1
        elif arabic_digit >= 5:
            if self.symbol5 is None:
                raise Exception('Unsupported 5')
            return self.symbol5 + self.symbol1 * (arabic_digit - 5)
        elif arabic_digit == 4:
            if self.symbol5 is None:
                raise Exception('Unsupported 4')
            return self.symbol1 + self.symbol5
        elif arabic_digit > 0:
            return self.symbol1 * arabic_digit
        elif arabic_digit == 0:
            return ''
        else:
            raise Exception('Negative digit')

    def roman2arabic(self, roman_digit: str) -> int:
        if roman_digit not in self.all_digits.keys():
            return 0
        else:
            return self.all_digits[roman_digit]


radix3 = Baryga('M', None, None)
radix2 = Baryga('C', 'D', radix3)
radix1 = Baryga('X', 'L', radix2)
radix0 = Baryga('I', 'V', radix1)
radixes = [radix0, radix1, radix2, radix3]


def arabic2roman(arabic: int) -> str:
    number = arabic
    result = ''
    radix = 0
    while number > 0:
        digit = number % 10
        number //= 10
        result = radixes[radix].arabic2roman(digit) + result
        radix += 1
    return result


def roman2arabic(roman: str) -> int:
    number = roman
    result = 0
    multiplier = 1
    for radix in radixes:
        for i in range(len(number)):
            tail = number[i:]
            arabic = radix.roman2arabic(tail)
            if arabic != 0:
                number = number[:-len(tail)]
                result += arabic * multiplier
                break
        multiplier *= 10
    if len(number) == 0:
        return result
    else:
        raise Exception('Invalid Input')


def translate(text: str):
    try:
        try:
            x = float(text)
            if text.isdigit():
                return arabic2roman(int(text))
            else:
                raise Exception('Invalid Number')
        except ValueError:
            return roman2arabic(text)
    except Exception as e:
        return e.args[0]


def arabic_check(value: str) -> int:
    if value.isnumeric():
        return int(value)
    else:
        return roman2arabic(value)
