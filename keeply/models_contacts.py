import re
from collections import UserDict
from datetime import datetime


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату."""

    def __init__(self, value: str):
        if not self.validate_phone(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр.")
        super().__init__(value)

    @staticmethod
    def validate_phone(value: str) -> bool:
        return len(value) == 10 and value.isdigit()


class Email(Field):
    """Клас для зберігання email. Має валідацію формату за допомогою регулярних виразів."""

    def __init__(self, value: str):
        if not self.validate_email(value):
            raise ValueError("Некоректний формат email. Приклад: user@example.com")
        super().__init__(value)

    @staticmethod
    def validate_email(value: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, value) is not None


class Birthday(Field):
    """Клас для зберігання дня народження. Має валідацію формату DD.MM.YYYY."""

    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Некоректний формат дати. Використовуйте DD.MM.YYYY")


class Address(Field):
    """Клас для зберігання фізичної адреси контакту."""
    pass


class Record:
    """Клас для зберігання інформації про контакт."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return
        raise ValueError(f"Телефон {old_phone} не знайдено.")

    def find_phone(self, phone: str) -> Phone:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones) if self.phones else "Немає"
        email_str = self.email.value if self.email else "Немає"
        bday_str = self.birthday.value if self.birthday else "Немає"
        address_str = self.address.value if self.address else "Немає"
        return (f"Ім'я: {self.name.value} | Телефони: {phones_str} | "
                f"Email: {email_str} | ДН: {bday_str} | Адреса: {address_str}")


class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days: int) -> list:
        """Повертає список контактів, у яких день народження відбудеться через вказану кількість днів від поточної дати."""
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()

                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)

                days_until = (bday_this_year - today).days

                if 0 <= days_until <= days:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays