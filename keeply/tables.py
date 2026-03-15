from tabulate import tabulate
from colorama import Fore, Style, init
import math

def format_contacts_table(book, page: int = 1, page_size: int = 10) -> str:
    """
    Повертає красиву таблицю контактів (кольори + пагінація).
    Колонки: Name | Phones | Birthday | Email | Address

    Підтримує, навіть якщо в Record ще немає email/address:
    - record.email (Field або None)
    - record.address (Field або None)
    """
    if isinstance(book, list):
        records = book
    else:
        records = list(book.data.values())
    if not records:
        return "No contacts saved."

    records.sort(key=lambda r: r.name.value.lower())

    total = len(records)
    total_pages = max(1, math.ceil(total / page_size))

    if page < 1 or page > total_pages:
        raise ValueError(f"Page out of range. Enter page 1..{total_pages}.")

    start = (page - 1) * page_size
    end = start + page_size
    chunk = records[start:end]

    def dim_dash(value: str) -> str:
        return f"{Style.DIM}{value}{Style.RESET_ALL}"

    def colored_or_dash(value: str, color: str) -> str:
        if not value or value == "-":
            return dim_dash("-")
        return f"{color}{value}{Style.RESET_ALL}"

    rows = []
    for rec in chunk:
        # Name
        name = f"{Fore.CYAN}{rec.name.value}{Style.RESET_ALL}"

        # Phones
        phones_raw = "; ".join(p.value for p in rec.phones) if getattr(rec, "phones", None) else "-"
        phones = colored_or_dash(phones_raw, Fore.GREEN)

        # Birthday
        birthday_raw = str(rec.birthday) if getattr(rec, "birthday", None) else "-"
        birthday = colored_or_dash(birthday_raw, Fore.MAGENTA)

        # Email (може бути Field або None, або взагалі відсутнє)
        email_field = getattr(rec, "email", None)
        email_raw = str(email_field) if email_field else "-"
        email = colored_or_dash(email_raw, Fore.YELLOW)

        # Address (може бути Field або None, або взагалі відсутнє)
        address_field = getattr(rec, "address", None)
        address_raw = str(address_field) if address_field else "-"
        address = colored_or_dash(address_raw, Fore.BLUE)

        rows.append([name, phones, birthday, email, address])

    table = tabulate(
        rows,
        headers=[
            f"{Style.BRIGHT}Name{Style.RESET_ALL}",
            f"{Style.BRIGHT}Phones{Style.RESET_ALL}",
            f"{Style.BRIGHT}Birthday{Style.RESET_ALL}",
            f"{Style.BRIGHT}Email{Style.RESET_ALL}",
            f"{Style.BRIGHT}Address{Style.RESET_ALL}",
        ],
        tablefmt="fancy_grid",
        disable_numparse=True
    )

    footer = (
        f"\n{Style.DIM}Page {page}/{total_pages} | "
        f"Total contacts: {total}"
    )
    return table + footer

def format_notes_table(notes, page: int = 1, page_size: int = 10, text_limit: int = 60) -> str:
    if not notes:
        return "No notes saved."
    if isinstance(notes, list):
        items = [(note.title, note) for note in notes]
    else:
        items = list(notes.items())
        items.sort(key=lambda x: str(x[0]).lower())

    total = len(items)
    total_pages = max(1, math.ceil(total / page_size))
    if page < 1 or page > total_pages:
        raise ValueError(f"Page out of range. Enter page 1..{total_pages}.")

    start = (page - 1) * page_size
    end = start + page_size
    chunk = items[start:end]

    def dim_dash() -> str:
        return f"{Style.DIM}-{Style.RESET_ALL}"

    def colored_or_dash(value: str, color: str) -> str:
        if not value or value == "-":
            return dim_dash()
        return f"{color}{value}{Style.RESET_ALL}"

    def shorten(text: str) -> str:
        text = (text or "").replace("\n", " ").strip()
        if not text:
            return "-"
        if len(text) <= text_limit:
            return text
        return text[: text_limit - 1] + "…"

    def tag_to_str(tag) -> str:
        # якщо Tag має .value — беремо його, інакше str(tag)
        if hasattr(tag, "value") and not callable(getattr(tag, "value")):
            return str(getattr(tag, "value"))
        return str(tag)

    rows = []
    for title_key, note in chunk:
        title_raw = str(title_key).strip() or "-"
        text_raw = shorten(getattr(note, "text", ""))

        tags_list = getattr(note, "tags", [])
        tags_raw = ", ".join(tag_to_str(t) for t in tags_list) if tags_list else "-"

        rows.append([
            colored_or_dash(title_raw, Fore.CYAN),
            colored_or_dash(text_raw, Fore.GREEN),
            colored_or_dash(tags_raw, Fore.MAGENTA),
        ])

    table = tabulate(
        rows,
        headers=[
            f"{Style.BRIGHT}Title{Style.RESET_ALL}",
            f"{Style.BRIGHT}Text{Style.RESET_ALL}",
            f"{Style.BRIGHT}Tags{Style.RESET_ALL}",
        ],
        tablefmt="fancy_grid",
    )

    footer = (
        f"\n{Style.DIM}Page {page}/{total_pages} | "
        f"Total notes: {total}"
    )
    return table + footer