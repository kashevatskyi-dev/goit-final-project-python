from collections import UserDict

class Tag:
    #Клас для зберігання тегу (ключового слова) нотатки.
    def __init__(self, value):
        # Зберігаємо теги в нижньому регістрі без зайвих пробілів для зручного пошуку
        self.value = str(value).strip().lower()

    def __str__(self):
        return f"#{self.value}"
        
    def __eq__(self, other):
        # Дозволяє порівнювати об'єкти Tag між собою
        if isinstance(other, Tag):
            return self.value == other.value
        return False

class Note:
    #Клас для зберігання окремої нотатки.
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.tags = []

    def add_tag(self, tag_value):
        #Додає тег до нотатки, уникаючи дублікатів.
        new_tag = Tag(tag_value)
        if new_tag not in self.tags:
            self.tags.append(new_tag)

    def remove_tag(self, tag_value):
        #Видаляє тег за його значенням.
        tag_to_remove = Tag(tag_value)
        self.tags = [t for t in self.tags if t != tag_to_remove]

    def edit_text(self, new_text):
        #Змінює текст нотатки.
        self.text = new_text

    def __str__(self):
        tags_str = ", ".join(str(t) for t in self.tags) if self.tags else "Немає тегів"
        return (f"--- {self.title} ---\n"
                f"{self.text}\n"
                f"Теги: {tags_str}\n"
                f"{'-'*20}")

class NoteBook(UserDict):
    #Клас для зберігання та управління нотатками.
    
    def add_note(self, note: Note):
        #Додає нотатку до словника (ключ - заголовок нотатки).
        self.data[note.title] = note

    def find_note(self, title) -> Note:
        #Повертає нотатку за заголовком.
        return self.data.get(title)

    def delete_note(self, title):
        #Видаляє нотатку за заголовком.
        if title in self.data:
            del self.data[title]
            return True
        return False

    def search_by_text(self, query):
        #Шукає нотатки, в яких текст або заголовок містять пошуковий запит.
        query = query.lower()
        results = []
        for note in self.data.values():
            if query in note.title.lower() or query in note.text.lower():
                results.append(note)
        return results

    def search_by_tag(self, tag_query):
        #Шукає нотатки, які містять вказаний тег.
        tag_query = tag_query.lower()
        results = []
        for note in self.data.values():
            # Перевіряємо, чи є шуканий тег серед тегів нотатки
            if any(t.value == tag_query for t in note.tags):
                results.append(note)
        return results

    def sort_by_tags(self):
        #Сортує нотатки за їхніми тегами в алфавітному порядку. Нотатки без тегів опиняться в кінці списку.
        def sort_key(note):
            if note.tags:
                # Використовуємо перший тег за алфавітом для сортування цієї нотатки
                return min([t.value for t in note.tags])
            # Магічний рядок для того, щоб нотатки без тегів падали в кінець списку
            return "яяя_без_тегів"

        # Сортуємо значення словника і повертаємо список відсортованих нотаток
        sorted_notes = sorted(self.data.values(), key=sort_key)
        return sorted_notes