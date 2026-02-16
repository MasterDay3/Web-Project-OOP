from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ROMAN_MAP = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_arabic(roman):
    roman = roman.upper()
    total = 0
    prev = 0

    for ch in reversed(roman):
        if ch not in ROMAN_MAP:
            raise ValueError("Invalid Roman numeral")

        value = ROMAN_MAP[ch]
        if value < prev:
            total -= value
        else:
            total += value
            prev = value

    # перевірка коректності (IIII, VV і тд)
    if arabic_to_roman(total) != roman:
        raise ValueError("Invalid Roman numeral")

    return total


def arabic_to_roman(num):
    if not (1 <= num <= 3999):
        raise ValueError("Number out of range (1–3999)")

    values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    result = ""
    for value, symbol in values:
        while num >= value:
            result += symbol
            num -= value

    return result


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    from_type = data.get("from")
    value = data.get("value")

    try:
        if from_type == "roman":
            result = roman_to_arabic(value)
            return jsonify({"result": result})

        elif from_type == "arabic":
            if not str(value).isdigit():
                raise ValueError("Arabic number must be numeric")

            result = arabic_to_roman(int(value))
            return jsonify({"result": result})

        else:
            return jsonify({"error": "Invalid conversion type"}), 400

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run()
