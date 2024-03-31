from collections import UserDict
DEBUG = True
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):# Клас для зберігання імені контакту. Обов'язкове поле.
    # реалізація класу
		pass

class Phone(Field): #Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр)
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError('Value error')

class Record: #Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
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

book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

pawel_record = Record("Pawel")
pawel_record.add_phone("0577209449")
book.add_record(pawel_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    if DEBUG:
        print(f'[Выводим всю книгу]{record}')
    else:
        print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
if DEBUG:  
    print(f'[Поменяли номер] {john}')  # Виведення: Contact name: John, phones: 1112223333; 5555555555
else:
    print(john)
# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
if DEBUG:   
    print(f"[Нашли номер] {john.name}: {found_phone}")  # Виведення: 5555555555
else:
    print(f'{john.name}: {found_phone}')
# # Видалення запису Jane
book.delete("Jane")


if DEBUG:
    for name, record in book.data.items():
        print(f'[Остались только]{record}')
       