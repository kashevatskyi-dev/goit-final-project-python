from pathlib import Path
from keeply.models_contacts import AddressBook, Record
from keeply.models_notes import NoteBook, Note
from keeply.storage import save_data, load_data
from keeply.utils import input_error, get_closest_match
from keeply.tables import format_contacts_table, format_notes_table

# Визначаємо домашню директорію користувача та створюємо приховану папку .keeply
STORAGE_DIR = Path.home() / ".keeply"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Вказуємо повні шляхи до файлів даних
CONTACTS_FILE = STORAGE_DIR / "contacts.pkl"
NOTES_FILE = STORAGE_DIR / "notes.pkl"

# Повний список валідних команд для інтелектуального вгадування
VALID_COMMANDS = [
    "hello", "close", "exit", 
    "add", "change", "phone", "all", "search-contact", "delete-contact",
    "add-email", "add-address", "add-birthday", "show-birthday", "birthdays",
    "add-note", "all-notes", "search-note", "edit-note", "delete-note", 
    "search-tag", "sort-tags", "add-tag", "remove-tag"
]

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

# ОБРОБНИКИ ДЛЯ КОНТАКТІВ

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "✅ Контакт оновлено."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "✅ Контакт додано."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "✅ Телефон оновлено."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.phones:
        return f"📱 Телефони {name}: {', '.join(p.value for p in record.phones)}"
    return f"У контакту {name} немає збережених телефонів."

@input_error
def show_all_contacts(args, book: AddressBook):
    if not book.data:
        return "📭 Адресна книга порожня."
    # return "\n".join(str(record) for record in book.data.values())
    page = 1
    if args:
        # all 2
        if len(args) != 1:
            raise ValueError("Usage: all [page]")
        if not args[0].isdigit():
            raise ValueError("Enter page number (e.g., all 2).")
        page = int(args[0])

    return format_contacts_table(book, page=page, page_size=5)

@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_email(email)
    return "✅ Email додано."

@input_error
def add_address(args, book: AddressBook):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_address(address)
    return "✅ Адресу додано."

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "✅ День народження додано."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday:
        return f"🎂 День народження {name}: {record.birthday.value}"
    return f"У контакту {name} не вказано день народження."

@input_error
def get_birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7 
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"У найближчі {days} днів днів народжень немає."
    
    res = f"🎉 Дні народження у найближчі {days} днів:\n"
    for record in upcoming:
        res += f"- {record.name.value} ({record.birthday.value})\n"
    return res.strip()

@input_error
def search_contact(args, book: AddressBook):
    query = args[0].lower()
    results = []
    for record in book.data.values():
        # Перевірка на збіги в імені, телефонах, email або адресі
        if (query in record.name.value.lower() or
            any(query in p.value for p in record.phones) or
            (record.email and query in record.email.value.lower()) or
            (record.address and query in record.address.value.lower())):
            results.append(record)
    
    if not results:
        return f"🔍 Контактів за запитом '{query}' не знайдено."
    # return "\n".join(str(r) for r in results)
    return format_contacts_table(results)

@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    if book.find(name):
        book.delete(name)
        return f"🗑️ Контакт {name} видалено."
    raise KeyError

# ОБРОБНИКИ ДЛЯ НОТАТОК

@input_error
def add_note(args, notebook: NoteBook):
    title = args[0]
    text_parts = [word for word in args[1:] if not word.startswith('#')]
    tags = [word[1:] for word in args[1:] if word.startswith('#')]
    
    note = Note(title, " ".join(text_parts))
    for tag in tags:
        note.add_tag(tag)
        
    notebook.add_note(note)
    return f"✅ Нотатку '{title}' успішно додано!"

@input_error
def show_all_notes(args, notebook: NoteBook):
    if not notebook.data:
        return "📭 Зошит з нотатками порожній."
    # return "\n".join(str(note) for note in notebook.data.values())
    page = 1
    if args:
        # all 2
        if len(args) != 1:
            raise ValueError("Usage: all [page]")
        if not args[0].isdigit():
            raise ValueError("Enter page number (e.g., all 2).")
        page = int(args[0])
    return format_notes_table(notebook, page=page, page_size=5)

@input_error
def search_note(args, notebook: NoteBook):
    query = " ".join(args)
    results = notebook.search_by_text(query)
    if not results:
        return f"🔍 Нотаток за запитом '{query}' не знайдено."
    # return "\n".join(str(note) for note in results)
    return format_notes_table(results)

@input_error
def search_by_tag(args, notebook: NoteBook):
    tag = args[0].replace('#', '')
    results = notebook.search_by_tag(tag)
    if not results:
        return f"🔍 Нотаток з тегом #{tag} не знайдено."
    # return "\n".join(str(note) for note in results)
    return format_notes_table(results)

@input_error
def sort_notes_by_tags(notebook: NoteBook):
    sorted_notes = notebook.sort_by_tags()
    if not sorted_notes:
        return "📭 Список нотаток порожній."
    # return "\n".join(str(note) for note in sorted_notes)
    return format_notes_table(sorted_notes)

@input_error
def edit_note(args, notebook: NoteBook):
    title = args[0]
    new_text = " ".join(args[1:])
    note = notebook.find_note(title)
    if not note:
        return f"❌ Нотатку з заголовком '{title}' не знайдено."
    note.edit_text(new_text)
    return f"✅ Текст нотатки '{title}' оновлено."

@input_error
def delete_note(args, notebook: NoteBook):
    title = args[0]
    if notebook.delete_note(title):
        return f"🗑️ Нотатку '{title}' видалено."
    return f"❌ Нотатку з заголовком '{title}' не знайдено."

@input_error
def add_tags_to_note(args, notebook: NoteBook):
    if len(args) < 2:
        raise ValueError("Введіть заголовок нотатки та хоча б один тег (з #).")
    title = args[0]
    tags = [word[1:] for word in args[1:] if word.startswith('#')]
    if not tags:
        raise ValueError("Теги повинні починатися з символу #.")
    note = notebook.find_note(title)
    if not note:
        return f"❌ Нотатку з заголовком '{title}' не знайдено."
    for tag in tags:
        note.add_tag(tag)
    return f"✅ Теги успішно додано до нотатки '{title}'."

@input_error
def remove_tag_from_note(args, notebook: NoteBook):
    if len(args) < 2:
        raise ValueError("Введіть заголовок нотатки та тег для видалення.")
    title = args[0]
    tag_to_remove = args[1].replace('#', '')
    note = notebook.find_note(title)
    if not note:
        return f"❌ Нотатку з заголовком '{title}' не знайдено."
    note.remove_tag(tag_to_remove)
    return f"✅ Тег #{tag_to_remove} видалено з нотатки '{title}'."

# ГОЛОВНИЙ ЦИКЛ ПРОГРАМИ

def main():
    contacts_book = load_data(CONTACTS_FILE, AddressBook)
    notes_book = load_data(NOTES_FILE, NoteBook)
    
    print("🤖 Вітаю! Я Keeply - твій персональний помічник. Введи команду (або 'hello').")
    
    while True:
        user_input = input("\n> ")
        if not user_input.strip():
            continue
            
        command, *args = parse_input(user_input)

        # Системні команди
        if command in ["close", "exit"]:
            save_data(contacts_book, CONTACTS_FILE)
            save_data(notes_book, NOTES_FILE)
            print("💾 Дані збережено. До зустрічі!")
            break
        elif command == "hello":
            print("Чим можу допомогти?")
            
        # Команди для контактів
        elif command == "add":
            print(add_contact(args, contacts_book))
        elif command == "change":
            print(change_contact(args, contacts_book))
        elif command == "phone":
            print(show_phone(args, contacts_book))
        elif command == "all":
            print(show_all_contacts(args, contacts_book))
        elif command == "add-email":
            print(add_email(args, contacts_book))
        elif command == "add-address":
            print(add_address(args, contacts_book))
        elif command == "add-birthday":
            print(add_birthday(args, contacts_book))
        elif command == "show-birthday":
            print(show_birthday(args, contacts_book))
        elif command == "birthdays":
            print(get_birthdays(args, contacts_book))
        elif command == "search-contact":
            print(search_contact(args, contacts_book))
        elif command == "delete-contact":
            print(delete_contact(args, contacts_book))
            
        # Команди для нотаток
        elif command == "add-note":
            print(add_note(args, notes_book))
        elif command == "all-notes":
            print(show_all_notes(args, notes_book))
        elif command == "search-note":
            print(search_note(args, notes_book))
        elif command == "search-tag":
            print(search_by_tag(args, notes_book))
        elif command == "sort-tags":
            print(sort_notes_by_tags(notes_book))
        elif command == "edit-note":
            print(edit_note(args, notes_book))
        elif command == "delete-note":
            print(delete_note(args, notes_book))
        elif command == "add-tag":
            print(add_tags_to_note(args, notes_book))
        elif command == "remove-tag":
            print(remove_tag_from_note(args, notes_book))
            
        # Невідома команда (Інтелектуальний аналіз)
        else:
            guess = get_closest_match(command, VALID_COMMANDS)
            if guess:
                print(f"❌ Невідома команда '{command}'. Можливо, ви мали на увазі: '{guess}'?")
            else:
                print("❌ Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()