from datetime import datetime

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper

class Birthday:
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = name
        self.phones = []
        self.birthday = None

    def add_birthday(self, value):
        self.birthday = Birthday(value)

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def find(self, name):
        for record in self.records:
            if record.name == name:
                return record
        return None

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name, = args
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.date.strftime('%d.%m.%Y')}."
    elif record:
        return f"{name} doesn't have a birthday set."
    return "Contact not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = []
    today = datetime.now().date()
    for record in book.records:
        if record.birthday:
            next_birthday = datetime(today.year, record.birthday.date.month, record.birthday.date.day).date()
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, record.birthday.date.month, record.birthday.date.day).date()
            days_until_birthday = (next_birthday - today).days
            if days_until_birthday <= 7:
                upcoming_birthdays.append((record.name, next_birthday))
    upcoming_birthdays.sort(key=lambda x: x[1])
    if upcoming_birthdays:
        return "\n".join([f"{name}'s birthday is on {date.strftime('%d.%m.%Y')}" for name, date in upcoming_birthdays])
    return "No upcoming birthdays."

def parse_input(user_input):
    user_input = user_input.strip().split(maxsplit=1)
    command = user_input[0]
    args = user_input[1].split() if len(user_input) > 1 else []
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
