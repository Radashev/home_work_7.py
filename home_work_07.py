from collections import defaultdict, UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value) 
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError('Invalid phone number')


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
           raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        # Phone('0951111111') == '0951111111'
        self.phones = [p for p in self.phones if str(p) != phone_number]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


    def find_next_birthday(self, weekday):
    
        pass

    def get_upcoming_birthday(self, days=7):
        self.days = upcoming_birthdays
        upcoming_birthdays = []
        today = datetime.today()
        next_week = today + timedelta(days=7)
        for record in self.records:
            if isinstance(record.birthday, Birthday) and record.birthday.value.date() <= next_week.date():
                upcoming_birthdays.append(record)
        return upcoming_birthdays


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid arguments. Usage: add [name] [phone_number]"
        except IndexError:
            return "Not enough arguments provided."
    return wrapper


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_contact(phone)
    return message



@input_error
def change_contact(args, book: AddressBook):
    """
    Змінює номер телефону для вказаного імені.
    """
    name, new_phone_number = args
    if name in book.data:
        book.data[name].phones = [Phone(new_phone_number)]
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phones(args, book: AddressBook):
    """
    Показує номер телефону для вказаного імені.
    """
    name = args[0]
    if name in book.data:
        return book.data[name].phones[0].value
    else:
        return "Contact not found."

@input_error
def show_all(args, book: AddressBook):
    """
    Показує всі контакти.
    """
    if book.data:
        return "\n".join(str(record) for record in book.data.values())
    else:
        return "No contacts found."

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Usage: add-birthday <contact_name> <birthday>")
    
    contact_name = args[0]
    birthday_str = args[1]

    # Знаходимо контакт за ім'ям
    contact = book.find(contact_name)
    if contact:
        contact.add_birthday(birthday_str)
        return "Birthday added."
    else:
        return f"Contact '{contact_name}' not found."


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Usage: show-birthday <contact_name>")
    
    contact_name = args[0]

    # Знаходимо контакт за ім'ям
    contact = book.find(contact_name)
    if contact and contact.birthday:
        return f"{contact_name}'s birthday is on {contact.birthday.value}"
    else:
        return f"No birthday found for '{contact_name}'."

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthday()
    if not upcoming_birthdays:
        return "No upcoming birthdays for next week"
    else:
        return "\n".join([f"{record.name.value}: {record.birthday.value.strftime('%d.%m.%Y')}" for record in upcoming_birthdays])


@input_error
def parse_input(user_input):
    """
    Функція розбирає введений користувачем рядок на команду та її аргументи.
    """
    parts = user_input.split()
    command = parts[0].lower()  # перша частина рядка - команда
    args = parts[1:]  # решта частин рядка - аргументи
    return command, args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command == "exit" or command == "close":
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))
            
        elif command == "all":
            print(show_all(args, book))

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