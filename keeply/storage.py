import pickle
import os
from typing import Any


def save_data(data: Any, filename: str) -> None:
    """Універсальна функція для збереження будь-яких даних у бінарний файл."""
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_data(filename: str, default_class: type) -> Any:
    """
    Універсальна функція для завантаження даних з файлу.
    Якщо файлу не існує або він пошкоджений, створює порожній об'єкт.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            print(f"Попередження: Файл {filename} пошкоджено. Створено нову базу даних.")
            return default_class()

    return default_class()