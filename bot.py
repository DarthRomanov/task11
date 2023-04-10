from collections import UserDict
import datetime


class Field():
    def __init__(self, value):
        self.value = value

    
    def __repr__(self):
        return f"{self.value}"
    

    
class Name(Field):
    pass
    

class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value = int(new_value)
        except ValueError:
            raise ValueError('Only numbers accepted')
        
    
    
    

class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value = datetime(new_value)
        except ValueError:
            raise ValueError('Only date accepted')  
   


class Record:
    def __init__(self, name:Name, phone:Phone=None, birthday:Birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.__birthday = birthday if birthday else None
    def add_phone(self, phone:Phone):
        self.phones.append(phone)
    def add_bibirthday(self, birthday:Birthday):
        self.__birthday = birthday

    
    def change_phone(self, old_phone:Phone,  new_phone:Phone):
        for i, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[i] = new_phone
                return f'Phone {old_phone} changed to phone {new_phone}'
            
    def delete_phone(self, phone):
        for i, p in enumerate(self.phones):
            if phone.value == p.value:
                self.phones[i] = None
                return f'phone {phone} was deleted'
    
    def days_to_birthday(self):
        if self.__birthday:
            Y_E = datetime.now(' %Y')
            n_b = self.__birthday + Y_E + 1
            d_n = datetime.now('%d, %m, %Y')
            result =  n_b - d_n
            return result
        return None
        
       

class AddressBook(UserDict):
    
    def add_record(self, record:Record):
        self.data[record.name.value] = record
        return f"Contact with name {record.name} added successfully"
    
    def __str__(self) -> str:
        return '\n'.join([f'{r.name} : {r.phones}' for r in self.data.values()])
    
    def iterator(self, page=3):
        start = 0

        while True:
            result = list(self.data)[start: start + page]

            if not result:
                break
            yield result
            start += page

    
   
contacts = AddressBook()



def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params"
        except KeyError:
            return "No contact whith this name"
        except ValueError:
            return "Fail, try again"
    return inner


def hello(*args):
    return "How can I help you?"

@input_error    
def add_ct(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    if len(args[2]) == 0:
        rec = Record(name, phone)
    else:
        birthday = Birthday(args[2])
        rec = Record(name, phone, birthday)
    return contacts.add_record(rec)

@input_error    
def change(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = contacts.get(name.value)
    if rec:
        return rec.change_phone(phone, new_phone)
    return f'No record with name {name}'

def delete(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = contacts.get(name.value)
    rec.delete_phone(phone)
    if rec:
        return rec.delete_phone(phone)
    return f'No record with name {name}'

def birthday_date(*args):
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec = contacts.get(name.value)
    if rec:
        return rec.add_bibirthday(birthday)
    return f'No record with name {name}'
    


def to_birthday(*args):
    name = Name(args[0])
    rec = Record(name)
    rec.days_to_birthday
    
    
    
@input_error
def phone_(*args):
    return contacts[args[0]]

def show_all(*args):
    iter = contacts.iterator()
    
    for rec in iter:
        n_s = []
        for i in rec:
            n_s.append(f"{i} : {contacts[i]}")
        print(n_s)
    

def exit(*args):
    return 'Bye'

def no_command(*args):
    return 'Unknown command. Try again'

def parse_input(text):
    text_command = text.split()[0].lower()
    match text_command:
        case 'hello':
            return hello, text.replace('hello', '').split()
        case 'time':
            return to_birthday, text.replace('birthday', '').split()
        case 'birthday':
            return birthday_date, text.replace('birthday', '').split()
        
        case 'add':
            return add_ct, text[len('add'):].split()
        case 'change':
            return change, text[len('change'):].split()
        case 'delete':
            return delete, text[len('change'):].split()
        
        case 'phone':
            return phone_, text[len('phone'):].split()
        case 'show':
            if text.split()[1].lower() == 'all':
                return show_all, str.lower(text).replace('show all', '').split()
        case 'exit':
            return exit, text[len('exit'):].split()
    return no_command, []
    

def main():
    while True:
        user_input = input(">>>")
        
        command, data = parse_input(user_input)
        
        print(command(*data))
        
        if command == exit:
            break

    

if __name__ == '__main__':
    main()