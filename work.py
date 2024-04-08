from collections import UserDict
from datetime import datetime,timedelta
DEBUG = False
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):# Клас для зберігання імені контакту. Обов'язкове поле.
    pass
		

class Phone(Field): #Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр)
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self,value):
        if len(value) == 10 and value.isdigit():
            self.__value = value  
        else:
            raise ValueError('Value error')
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record: #Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів і день його народження
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_birthday(self, birthday ):
        birthday = Birthday(birthday)  
        
       
    def __str__(self):
        
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {str(self.birthday)}"

    def add_phone(self, phone_number): # Додаємо тел
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number): # Видаляємо тел
        self.phones = [p for p in self.phones if str(p) != phone_number]

    def edit_phone(self,old_num, new_num):# редагування номеру
        for i, num in enumerate(self.phones):
            if str(num) == old_num:
                self.phones[i] = Phone(new_num)
                break
            else:
                raise ValueError('Value erorr')
        
    def find_phone(self, find_num): # Пошук номеру
        for i,num in enumerate(self.phones):
            if str(num)  == find_num:
                return num

class AddressBook(UserDict): #Клас для зберігання та управління записами.
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):# який знаходить запис за ім'ям
        return self.data.get(name)

    def delete(self, name):# який видаляє запис за ім'ям.
        return self.data.pop(name)
    
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values()) 
    
    def get_upcoming_birthdays(users:list) -> list: # повертає список користувачів, яких потрібно привітати по днях на наступному тижні. Сюда передать Список с словарем
        TODAY_DATE = datetime.today().date()
        n_upcoming_birthdays = []

        for user in users:
            user['birthday'] = datetime.strptime(user['birthday'], '%Y.%m.%d').date()

        for user in users:
            # Тут присвоим наш 2024 год учаснику для проверки дальше . / 2012-03-01 -> 2024-03-01
            birthday_this_year = user["birthday"].replace(year=TODAY_DATE.year)

            #  Проверка не прошел день рождения
            if birthday_this_year < TODAY_DATE:
                birthday_this_year = birthday_this_year.replace(year=TODAY_DATE.year + 1)
            
            # Проверяем попадет ли день на суботу или воскресенье
            if (birthday_this_year.weekday() == 5):  # Субота
                    birthday_this_year += timedelta(days=2)  # Переход на следущий понедельник

            elif (birthday_this_year.weekday() == 6):  # Воскресенье
                    birthday_this_year += timedelta(days=1)  # Переход на следущий понедельник

            # Тут будет разница между Днем рождения и сегодняшним днем для сравнения дальше
            count_day = (birthday_this_year - TODAY_DATE).days

            # Сохраняем дату имя персонажа и дату если оно <= 7 
            if count_day == 0 or count_day <= 7:
                n_upcoming_birthdays.append({"name": user["name"], "congratulation_date": birthday_this_year})

        return n_upcoming_birthdays
    
def parse_input(user_input): # Тут мы парсим строку в нижний регистр
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):# Це наш декоратор
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return 'Enter the argument for the command'
        except IndexError:
            return 'Enter the argument for the command'

    return inner

@input_error
def add_contact(args, book: AddressBook): # Тут мы додаем номер и имя

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
def change_contact(args, book:AddressBook): # Тут мы меняем старый номер на новый
    name, phone, *_ = args
    record = book.find(name)
    if record:
        record = Record(name)
        book.add_record(record)
    if phone:
        record.add_phone(phone)
    return "Contact added replace."

@input_error
def show_phone(args, book:AddressBook): # Тут мы выводим номер указаного человека по ключу
    name = args[0]
    record = book.find(name)
    return record

@input_error
def show_all(book: AddressBook): # Тут ми повертаємо book в любому вигляді
    return book
    
@input_error
def add_birthday(args, book:AddressBook): # Додати дату народження для вказаного контакту.
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record:
        record.birthday = Record(birthday)
        return message
    else:
        None
    
        
    
@input_error
def show_birthday(args, book:AddressBook): # Показати дату народження для вказаного контакту.
    # реалізація Аналог show_phone
    pass

@input_error
def birthdays(args, book:AddressBook): # Показати дні народження, які відбудуться протягом наступного тижня.
    # реалізація
    pass

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

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

