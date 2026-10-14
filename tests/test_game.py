import os
import random
from unittest.mock import patch
# Предполагается, что код вашей игры сохранен в файле game.py
from game import Game, save_game, load_game, _dict

# Фиксируем индекс слова 'Python' для предсказуемости тестов
KEYS = list(_dict.keys())
PYTHON_INDEX = KEYS.index('Python')


def test_initialization():
    """Проверка правильной инициализации игры."""
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()
    
    assert game.secret == 'Python'
    assert game.mask == ['*', '*', '*', '*', '*', '*']
    assert game.guessed == set()
    assert game.message == ""
    assert game.get_describe() == 'Язык программирования'


def test_check_letter_empty():
    """Проверка ввода пустой строки или пробелов."""
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()
        
    game.check_letter("")
    assert game.message == "Вы ничего не ввели!"

    game.check_letter("   ")
    assert game.message == "Вы ничего не ввели!"


def test_check_letter_hit():
    """Проверка успешного угадывания буквы (включая регистр)."""
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()

    # Угадываем маленькую 'y'
    game.check_letter('y')
    assert 'Y' in game.guessed
    assert game.mask[1] == 'y'
    assert "есть в слове" in game.message

    # Угадываем маленькую 'p', которая в слове заглавная 'P'
    game.check_letter('p')
    assert game.mask[0] == 'P'  # Оригинальный регистр сохранен
    assert "есть в слове" in game.message


def test_check_letter_miss():
    """Проверка ввода буквы, которой нет в слове."""
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()

    game.check_letter('z')
    assert 'Z' in game.guessed
    assert "нет в слове" in game.message
    assert game.mask == ['*', '*', '*', '*', '*', '*']


def test_check_letter_already_guessed():
    """Проверка предупреждения при повторном вводе буквы."""
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()

    game.check_letter('y')
    game.check_letter('Y')  # Повторный ввод в другом регистре
    assert "уже угадывалась" in game.message


def test_is_finished():
    """Проверка триггера завершения игры."""
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()

    assert game.is_finished() is False

    # Отгадываем все буквы слова 'Python'
    for letter in ['p', 'y', 't', 'h', 'o', 'n']:
        game.check_letter(letter)

    assert game.is_finished() is True


def test_save_and_load_game():
    """Проверка сохранения и загрузки состояния игры."""
    path = 'test_save.pkl'
    
    with patch('random.randint', return_value=PYTHON_INDEX):
        game = Game()

    game.check_letter('p')
    game.check_letter('z')
    
    try:
        save_game(game, path)
        assert os.path.exists(path)

        loaded_game = load_game(path)

        assert loaded_game.secret == game.secret
        assert loaded_game.mask == game.mask
        assert loaded_game.guessed == game.guessed
        assert isinstance(loaded_game.guessed, set)
    finally:
        # Гарантированно удаляем временный файл после теста
        if os.path.exists(path):
            os.remove(path)
