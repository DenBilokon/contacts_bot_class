from collections import UserDict
from decorators import *

HELP_TEXT = """This contact bot save your contacts 
    Global commands:
      'add' - add new contact. Input user name and phone
    Example: add User_name 095-xxx-xx-xx
      'change' - change users old phone to new phone. Input user name, old phone and new phone
    Example: change User_name 095-xxx-xx-xx 050-xxx-xx-xx
      'delete' - delete contact (name and phones). Input user name
    Example: delete User_name
      'phone' - show contacts of input user. Input user name
    Example: phone User_name
      'show all' - show all contacts
    Example: show all
      'exit/'.'/'bye'/'good bye'/'close' - exit bot
    Example: good bye"""


class AddressBook(UserDict):
    """ Dictionary class """

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_rec(self, name):
        return f'{name} : {", ".join([phone.value for phone in self.data[name].phones])}'

    def show_all_rec(self):
        return "\n".join(f'{rec.name} : {", ".join([p.value for p in rec.phones])}' for rec in self.data.values())

    def change_record(self, name_user, old_record_num, new_record_num):
        record = self.data.get(name_user)
        if record:
            record.change(old_record_num, new_record_num)


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return self.value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    """Class for do phone number standard type"""

    @staticmethod
    def sanitize_phone_number(phone_user):
        new_phone = (
            phone_user.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        return new_phone

    def __init__(self, phone):
        sanitized_phone_number = Phone.sanitize_phone_number(phone)
        super().__init__(sanitized_phone_number)


class Record:
    """ Class for record name or phones"""

    def __init__(self, name, phone=None):
        self.name = name
        self.phone = phone
        self.phones = list()
        if isinstance(phone, Phone):
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def change(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                self.phones.remove(phone)
                self.phones.append(Phone(new_phone))
                return
        print(f"Phone {old_phone} not found in the Record")


ADDRESSBOOK = AddressBook()


def hello(*args):
    return "How can I help you?"


# Exit assistant
def bye(*args):
    return "Bye"


# README instructions
def help_user(*args):
    return HELP_TEXT


# Add user or user with phone to AddressBook
@input_error
def add(*args):
    name = Name(str(args[0]).title())
    phone_num = Phone(args[1])
    rec = ADDRESSBOOK.get(name.value)
    if rec:
        rec.add_phone(phone_num)
    else:
        rec = Record(name, phone_num)
        ADDRESSBOOK.add_record(rec)
    return f'Contact {name} {phone_num} added'


# Change users contact to another contact
@input_error
def change(*args):
    name = str(args[0]).title()
    old_phone = args[1]
    new_phone = args[2]
    ADDRESSBOOK.change_record(name, old_phone, new_phone)
    return f'Contact {name} {old_phone} to {new_phone} changed'


# Delete contact
@input_error
def delete_contact(*args):
    name = Name(str(args[0]).title())
    rec = Record(name)
    ADDRESSBOOK.remove_record(rec)
    return f'Contact {name} deleted'


# Show some contact
def phone(*args):
    return ADDRESSBOOK.show_rec(str(args[0]).title())


# Show all contacts
def show_all(*args):
    return ADDRESSBOOK.show_all_rec()


COMMANDS = {
    hello: ["hello", "hi"],
    show_all: ["show all"],
    phone: ["phone"],
    add: ["add"],
    change: ["change"],
    delete_contact: ["delete"],
    help_user: ["help"],
    bye: [".", "bye", "good bye", "close", "exit"],
}


def parse_command(text: str):
    for comm, key_words in COMMANDS.items():
        for key_word in key_words:
            if text.startswith(key_word):
                return comm, text.replace(key_word, "").strip().split(" ")
    return None, None


# ?????????????? ?????????????????????? ?? ???????????? ?? ?????????????????? ?????????????? ???????????????????? ???? ??????????????
def run_bot(user_input):
    command, data = parse_command(user_input.lower())
    if not command:
        return "Incorrect input. Try again"
    return command(*data)


def main():

    while True:
        user_input = str(input(">>>> "))
        result = run_bot(user_input)
        if result == "Bye":
            print("Goodbye!")
            break
        print(result)


if __name__ == "__main__":

    main()
