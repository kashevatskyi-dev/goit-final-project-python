import pickle
import os

def save_data(data, filename):
    #Універсальна функція для збереження будь-яких даних у бінарний файл.
    #data: об'єкт, який потрібно зберегти (AddressBook або NoteBook).
    #filename: ім'я файлу (наприклад, 'contacts.pkl' або 'notes.pkl').
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data(filename, default_class):
    #Універсальна функція для завантаження даних з файлу.
    #Якщо файлу не існує або він пошкоджений, створює порожній об'єкт.

    #filename: ім'я файлу для читання.
    #default_class: клас, екземпляр якого треба створити, якщо файлу немає (наприклад, AddressBook або NoteBook).

    # Перевіряємо, чи взагалі існує такий файл на диску
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except (EOFError, pickle.UnpicklingError):
            # Якщо файл порожній або пошкоджений, програма не впаде з помилкою, а просто почне з чистого аркуша.
            print(f"Попередження: Файл {filename} пошкоджено. Створено нову базу даних.")
            return default_class()
    
    # Якщо файлу немає (перший запуск програми), повертаємо новий порожній екземпляр
    return default_class()