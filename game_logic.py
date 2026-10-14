import random
import pickle

_dict = {
    'False': 'Логическое значение',
    'None': 'Пустой',
    'True': 'Истина',
    'Python': 'Язык программирования'
}

keys = list(_dict.keys())


class Game:
    def __init__(self):
        self.keys = keys
        self.ind = random.randint(0, len(self.keys) - 1)
        self.secret = self.keys[self.ind]
        # Для веб-интерфейса лучше хранить просто '*' без лишних пробелов
        self.mask = ['*'] * len(self.secret)
        self.guessed = set()
        self.message = ""  # Будем хранить уведомления для пользователя здесь

    def get_describe(self):
        return _dict[self.secret]

    def check_letter(self, letter):
        letter = letter.strip()
        if not letter:
            self.message = "Вы ничего не ввели!"
            return

        # Регистронезависимая проверка
        letter_upper = letter.upper()
        if letter_upper in self.guessed:
            self.message = f"Буква '{letter}' уже угадывалась!"
            return

        self.guessed.add(letter_upper)
        hit = False

        for i, ch in enumerate(self.secret):
            if ch.upper() == letter_upper:
                self.mask[i] = ch  # Сохраняем оригинальный регистр буквы из слова
                hit = True

        if hit:
            self.message = f"Отлично! Буква '{letter}' есть в слове."
        else:
            self.message = f"Увы, буквы '{letter}' нет в слове."

    def is_finished(self):
        return '*' not in self.mask

    def __getstate__(self):
        state = self.__dict__.copy()
        state['guessed'] = list(self.guessed)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.guessed = set(self.guessed)


# Функции сохранения/загрузки
def save_game(game, path='save_game.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(game, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_game(path='save_game.pkl'):
    with open(path, 'rb') as f:
        return pickle.load(f)