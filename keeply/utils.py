import difflib
from typing import Callable, Any, List, Optional

def input_error(func: Callable) -> Callable:
    """Декоратор для перехоплення та обробки помилок вводу."""
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"❌ Помилка: {e}"
        except KeyError:
            return "❌ Помилка: Контакт або нотатку не знайдено."
        except IndexError:
            return "❌ Помилка: Недостатньо аргументів для команди."
        except Exception as e:
            return f"❌ Неочікувана помилка: {e}"
    return inner

def get_closest_match(command: str, valid_commands: List[str]) -> Optional[str]:
    """
    Знаходить найближчу команду зі списку валідних команд, якщо користувач зробив одруківку (наприклад 'ad' замість 'add').
    difflib.get_close_matches повертає список співпадінь.
    cutoff=0.6 означає, що слова мають бути схожі мінімум на 60%.
    """
    matches = difflib.get_close_matches(command, valid_commands, n=1, cutoff=0.6)
    return matches[0] if matches else None