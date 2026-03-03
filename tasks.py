# tasks.py
import csv
import random
from numsystems import Convertor


class TaskGenerator:
    """Генерує задачі multiple choice для різних систем числення."""

    SYSTEMS = ["roman", "arabic", "egyptian", "thai", "binary"]

    MISTAKES_FILE = "mistakes.csv"
    CSV_FIELDS = ["question", "answer", "system", "difficulty"]

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
 # ── MISTAKES CSV ───────────────────────────────────────────────────────
    def record_mistake(self, task: dict) -> None:
        """Зберігає завдання в CSV при неправильній відповіді (без дублів)."""
        mistakes = self._load_mistakes()
        already_exists = False
        for m in mistakes:
            if m["question"] == task["question"]:
                already_exists = True
                break
        if not already_exists:
            mistakes.append({k: task[k] for k in CSV_FIELDS})
            self._save_mistakes(mistakes)

    def retry_mistake(self, task: dict) -> dict:
        """
        Повертає те саме завдання з новими варіантами відповідей
        (1 правильна + 3 нові рандомні дистрактори).
        """
        low, high = self.DIFFICULTY_RANGES[task["difficulty"]]
        answer = task["answer"]

        if task["system"] == "arabic":
            # відповідь — римське число
            new_distractors: set[str] = set()
            while len(new_distractors) < 3:
                n = random.randint(low, min(high, 3999))
                r = Convertor(str(n)).convert_to_roman()
                if r != answer:
                    new_distractors.add(r)
        else:
            # відповідь — арабське число
            correct_int = int(answer)
            new_distractors: set[str] = set()
            attempts = 0
            while len(new_distractors) < 3 and attempts < 200:
                attempts += 1
                offset = random.randint(-15, 15)
                candidate = correct_int + offset
                if candidate != correct_int and low <= candidate <= high:
                    new_distractors.add(str(candidate))

        options = [answer] + list(new_distractors)[:3]
        random.shuffle(options)
        return {**task, "options": options}

    def check_mistake(self, task: dict, user_answer: str) -> bool:
        """
        Перевіряє повторну відповідь на «помилкове» завдання.
        Правильно → видаляє з CSV, повертає True.
        Неправильно → залишає в CSV, повертає False.
        """
        correct = task["answer"] == user_answer
        if correct:
            mistakes = self._load_mistakes()
            mistakes = [m for m in mistakes if m["question"] != task["question"]]
            self._save_mistakes(mistakes)
        return correct

    def get_mistake_tasks(self) -> list[dict]:
        """Повертає всі збережені помилкові завдання з новими варіантами відповідей."""
        return [self.retry_mistake(m) for m in self._load_mistakes()]

    def _load_mistakes(self) -> list[dict]:
        with open(MISTAKES_FILE, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _save_mistakes(self, mistakes: list[dict]) -> None:
        with open(MISTAKES_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(mistakes)
    
