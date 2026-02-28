# tasks.py
import random
from numsystems import Convertor


class TaskGenerator:
    """Генерує задачі multiple choice для різних систем числення."""

    SYSTEMS = ["roman", "arabic", "egyptian", "thai", "binary"]

    DIFFICULTY_RANGES = {
        "easy": (1, 20),
        "medium": (21, 100),
        "hard": (101, 3999),
    }

    def generate(self, system: str, difficulty: str = "easy") -> dict:
        """
        Повертає словник:
        {
            'question': 'Що таке XIV?',
            'options':  ['14', '16', '9', '40'],  # перемішані
            'answer':   '14',
            'system':   'roman',
            'difficulty': 'easy'
        }
        """
        low, high = self.DIFFICULTY_RANGES[difficulty]

        match system:
            case "roman":
                return self._roman_task(low, min(high, 3999), difficulty)
            case "arabic":
                return self._arabic_task(low, high, difficulty)
            case "egyptian":
                return self._egyptian_task(low, min(high, 9999999), difficulty)
            case "thai":
                return self._thai_task(low, high, difficulty)
            case "binary":
                return self._binary_task(low, high, difficulty)
            case _:
                raise ValueError(f"Невідома система: {system}")

    # ── ROMAN ──────────────────────────────────────────────────────────────
    def _roman_task(self, low, high, difficulty) -> dict:
        number = random.randint(low, high)
        roman = Convertor(str(number)).convert_to_roman()
        question = f"Що таке {roman} в арабських числах?"
        answer = str(number)
        distractors = self._arabic_distractors(number, low, high)
        return self._pack(question, answer, distractors, "roman", difficulty)

    # ── ARABIC ─────────────────────────────────────────────────────────────
    def _arabic_task(self, low, high, difficulty) -> dict:
        number = random.randint(low, high)
        roman = Convertor(str(number)).convert_to_roman()
        question = f"Що таке {number} в римських числах?"
        answer = roman

        # генеруємо 3 невірні римські числа
        distractors = set()
        while len(distractors) < 3:
            n = random.randint(low, min(high, 3999))
            r = Convertor(str(n)).convert_to_roman()
            if r != answer:
                distractors.add(r)

        return self._pack(question, answer, list(distractors), "arabic", difficulty)

    # ── EGYPTIAN ───────────────────────────────────────────────────────────
    def _egyptian_task(self, low, high, difficulty) -> dict:
        number = random.randint(low, min(high, 9999))
        egyptian = Convertor(str(number)).convert_to_egyptian()
        question = f"Що таке {egyptian} в арабських числах?"
        answer = str(number)
        distractors = self._arabic_distractors(number, low, high)
        return self._pack(question, answer, distractors, "egyptian", difficulty)

    # ── THAI ───────────────────────────────────────────────────────────────
    def _thai_task(self, low, high, difficulty) -> dict:
        number = random.randint(low, high)
        thai = Convertor(str(number)).convert_to_thai()
        question = f"Що таке {thai} в арабських числах?"
        answer = str(number)
        distractors = self._arabic_distractors(number, low, high)
        return self._pack(question, answer, distractors, "thai", difficulty)

    # ── BINARY ─────────────────────────────────────────────────────────────
    def _binary_task(self, low, high, difficulty) -> dict:
        number = random.randint(low, high)
        binary = bin(number)[2:]  # прибираємо '0b'
        question = f"Що таке {binary} в арабських числах?"
        answer = str(number)
        distractors = self._arabic_distractors(number, low, high)
        return self._pack(question, answer, distractors, "binary", difficulty)

    # ── HELPERS ────────────────────────────────────────────────────────────
    def _arabic_distractors(self, correct: int, low: int, high: int) -> list:
        """3 неправильні арабські числа близькі до правильного."""
        distractors = set()
        while len(distractors) < 3:
            offset = random.randint(-10, 10)
            candidate = correct + offset
            if candidate != correct and low <= candidate <= high:
                distractors.add(str(candidate))
        return list(distractors)

    def _pack(self, question, answer, distractors, system, difficulty) -> dict:
        """Збирає фінальний словник з перемішаними варіантами."""
        options = [answer] + distractors[:3]
        random.shuffle(options)
        return {
            "question": question,
            "options": options,
            "answer": answer,
            "system": system,
            "difficulty": difficulty,
        }
