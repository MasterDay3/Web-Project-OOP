import random
class Tasks:
    levels = ['easy', 'middle', 'hard', 'very_hard']

    def __init__(self, system, level='easy'):
        self.system = system
        if level not in self.levels:
            raise ValueError('No such tasks level')
        self.level = level
        self.score = 0

    def generate_lvl_task(self):
        lvl_tasks = []
        match self.system:
            case 'roman':
                filename = 'tasks/roman_math_tasks.csv'
            case 'thai':
                filename = 'tasks/thai_math_tasks.csv'
            case 'egyptian':
                filename = 'tasks/eguptian_math_tasks.csv'
            case _:
                return 'No such system yet'
        with open(filename, 'r', encoding = 'utf-8') as task_file:
            lines = task_file.readlines()
            for line in lines:
                if line.startswith('level'):
                    continue
                lvl, question, answer = line.split(',')
                if lvl != self.level:
                    continue
                else:
                    lvl_tasks.append((question, answer))
        return lvl_tasks

    def next_level(self):
        current_index = self.levels.index(self.level)
        if current_index + 1 < len(self.levels):
            self.level = self.levels[current_index + 1]
            self.score = 0
            return True
        return False

    def main(self):
        while True:
            print(f'Рівень: {self.level}, Правильних: {self.score}/5')
            tasks = self.generate_lvl_task()

            if not tasks:
                print(f'Немає завдань для рівня {self.level}')
                break

            question, correct_answer = random.choice(tasks)
            print(f'Завдання: {question}')
            user_answer = input('Ваша відповідь: ').strip().upper()

            if user_answer == correct_answer.strip().upper():
                self.score += 1
                print(f'Правильно! Рахунок: {self.score}/5')
            else:
                print(f'Неправильно. Правильна відповідь: {correct_answer}')

            if self.score >= 5:
                print(f'Чудово! Ви пройшли рівень {self.level}!')
                if self.next_level():
                    print(f'Переходимо на рівень: {self.level}')
                else:
                    print('Вітаємо! Ви пройшли всі рівні!')
                    break

# t = Tasks(system='roman', level = 'easy')
# t.main()
class DailyTasks:
    def __init__(self, system):
        self.system = system
