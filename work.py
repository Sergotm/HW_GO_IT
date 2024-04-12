from collections import UserDict
from datetime import datetime, timedelta

DEBUG = False


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):  # Клас для зберігання імені контакту. Обов'язкове поле.
    pass


class Phone(Field):  # Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр)
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
            raise ValueError('Value error')


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:  # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів і день його народження
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # def add_birthday(self, birthday ):
    #     birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {str(self.name.value)}, phones: {'; '.join(str(p) for p in self.phones)} birthday: {str(self.birthday)}"

    def add_phone(self, phone_number):  # Додаємо тел
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):  # Видаляємо тел
        self.phones = [p for p in self.phones if str(p) != phone_number]

    def edit_phone(self,old_num, new_num):# редагування номеру
        for i, num in enumerate(self.phones):
            if str(num) == old_num:
                self.phones[i] = Phone(new_num)
                break
        else:
            raise ValueError('Value erorr')

    def find_phone(self, find_num):  # Пошук номеру
        for i, num in enumerate(self.phones):
            if str(num) == find_num:
                return num


class AddressBook(UserDict):  # Клас для зберігання та управління записами.
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):  # який знаходить запис за ім'ям
        return self.data.get(name)

    def delete(self, name):  # який видаляє запис за ім'ям.
        return self.data.pop(name)

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

    def get_upcoming_birthdays(self, days=7) -> list:
        today = datetime.today().date()
        upcoming_birthdays = []

        for user in self.data.values():
            if user.birthday is None:
                continue
            birthday_this_year = user.birthday.value.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if 0 <= (birthday_this_year - today).days <= days:
                if (birthday_this_year.weekday() == 5):  # Субота
                    birthday_this_year += timedelta(days=2)
                    
                elif (birthday_this_year.weekday() == 6):  # Воскресенье
                    birthday_this_year += timedelta(days=1)

                congratulation_date_str = birthday_this_year.strftime("%Y.%m.%d")
                upcoming_birthdays.append(
                    {
                        "name": user.name.value,
                        "congratulation_date": congratulation_date_str,
                    }
                )

        return upcoming_birthdays


def parse_input(user_input):  # Тут мы парсим строку в нижний регистр
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):  # Це наш декоратор
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command ValueError"
        except KeyError:
            return 'Enter the argument for the command KeyError'
        except IndexError:
            return 'Enter the argument for the command IndexError'

    return inner


@input_error
def add_contact(args, book: AddressBook):  # Тут мы додаем номер и имя

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):  # Тут мы меняем старый номер на новый
    name, old_num, new_num = args
    record = book.find(name)

    if record:
        record.edit_phone(old_num, new_num)
    if not record:
        return 'Contact not exist'
    return "Contact added replace."


@input_error
def show_phone(args, book: AddressBook):  # Тут мы выводим номер указаного человека по ключу
    name = args[0]
    record = book.find(name)
    return record


@input_error
def show_all(book: AddressBook):  # Тут ми повертаємо book в любому вигляді
    return book


@input_error
def add_birthday(args, book: AddressBook):  # Додати дату народження для вказаного контакту.
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record:
        record.birthday = Birthday(birthday)
        return message
    else:
        None


@input_error
def show_birthday(args,
                  book: AddressBook):  # Показати дату народження для вказаного контакту.////////////////////////Не розумію як зробити це//////////////////////////////////
    '''Я розумію що потрібно день нарождення витягнути  із book але не розумію як це зробить'''
    name = args[0]
    record = book.find(name)
    return str(record.birthday)


@input_error
def birthdays(book: AddressBook):  # Показати дні народження, які відбудуться протягом наступного тижня.
    birthday = book.get_upcoming_birthdays()
    if not len(birthday):
        return "There are no upcoming birthdays."
    for day in birthday:
        print(f"{day}")
    


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:

        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == 'change':
            print(change_contact(args, book))

        elif command == 'phone':
            print(show_phone(args, book))

        elif command == 'all':
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthday":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

# add Serhii 1111111111
# add Serhii 2222222222
# change Serhii 1111111111 33333333333
# add-birthday Serhii 12.04.2000
# show-birthday Serhii

