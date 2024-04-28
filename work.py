from collections import UserDict
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import pickle

def save_data(book, filename="Home_WEB\\addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename="Home_WEB\\addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

class Messager(ABC):
    @abstractmethod
    def send_to_user(self, massage:str)-> None:
        pass

class TerminalMessanger(Messager):
    def send_to_user(self, massage: str) -> None:
        print(massage)

class WebMessanger(Messager):
    def send_to_user(self, massage: str) -> None:
        print(f'Fake output to Web{massage}')

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
        return f""" {'_'*25}\n|Contact name: {str(self.name.value)}\n|Phones: {'; '.join(str(p) for p in self.phones)}\n|Birthday: {str(self.birthday)}\n|{'_'*25} """

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
                  book: AddressBook):  # Показати дату народження для вказаного контакту
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

def see_command():
    return f'''
 {'_'*54}
|hello         |How can I help you?                    |\n|{'_'*54}|
|add           |Contact added                          |\n|{'_'*54}|
|change        |Contact replace                        |\n|{'_'*54}| 
|phone         |Look at the phone                      |\n|{'_'*54}|           
|all           |Look at the addres book                |\n|{'_'*54}|            
|add-birthday  |Birthday added                         |\n|{'_'*54}|       
|show-birthday |Look at the day birthday users         |\n|{'_'*54}|                    
|birthday      |Look at the day birthday in the week   |\n|{'_'*54}|                    
|close / exit  |Close or exit program                  |\n|{'_'*54}|
'''

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    print(f" {'_'*43}\n|see_command - Look all the command program |\n|{'_'*43}|")
    messander = None

    while messander == None:
        user_qestion = input(f'Choose interface: 1 = Terminal, 2 = Web \n')
        if user_qestion == '1':
            messander = TerminalMessanger()
        elif user_qestion == '2':
            messander = WebMessanger()
        else:
            print(f'Incorrect data')
            messander = None
            continue

    while True:
        try:
            
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                messander.send_to_user("Good bye!")
                break
            elif command == "hello":
                messander.send_to_user("How can I help you?")

            elif command == "add":
                messander.send_to_user(add_contact(args, book))

            elif command == 'change':
                messander.send_to_user(change_contact(args, book))

            elif command == 'phone':
                messander.send_to_user(show_phone(args, book))

            elif command == 'all':
                messander.send_to_user(show_all(book))

            elif command == "add-birthday":
                messander.send_to_user(add_birthday(args, book))

            elif command == "show-birthday":
                messander.send_to_user(show_birthday(args, book))

            elif command == "birthday":
                messander.send_to_user(birthdays(book))

            elif command == 'see_command':
                messander.send_to_user(see_command())
            
            else:
                messander.send_to_user("Invalid command.")

            save_data(book)
        except KeyboardInterrupt:
            save_data(book)

if __name__ == "__main__":
    main()

# add Serhii 1111111111
# add Serhii 2222222222
# change Serhii 1111111111 33333333333
# add-birthday Serhii 12.04.2000
# show-birthday Serhii

