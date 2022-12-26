from collections import UserDict
from decorators import *

HELP_TEXT = """This contact bot save your contacts 
    Global commands:
      'add' - add new contact. Input user name and phone
    Example: add User_name 095-xxx-xx-xx
      'change' - change users old phone to new phone. Input user name, old phone and new phone
    Example: change User_name 095-xxx-xx-xx 050-xxx-xx-xx
      'phone' - show contacts of input user. Input user name
    Example: phone User_name
      'show all' - show all contacts
    Example: show all
      'exit/'.'/'bye'/'good bye'/'close' - exit bot
    Example: good bye"""


class AddressBook(UserDict):
    def add_record(self, record, *args):
        self.data[record.name.value] = record

    def remove_record(self, record, *args):
        self.data.pop(record.name.value, None)

    def show_rec(self, record_name, *args):
        return self.data[record_name].show_all()

    def show_all_rec(self):
        return "\n".join(
            [
                f'{rec.name} : {", ".join([p.value for p in rec.phones])}'
                for rec in self.data.values()
            ]
        )

    def change_record(self, name, old_record_num, new_record_num):
        record = self.data.get(name)
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
    @staticmethod
    def sanitize_phone_number(phone):
        new_phone = (
            phone.strip()
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
    def __init__(self, name, phone=None):
        self.name = name
        self.phones = list()
        if phone:
            self.phones.append(phone)


ADDRESSBOOK = AddressBook()


def hello(*args):
    return "How can I help you?"


def bye(*args):
    return "Bye"


def help_user(*args):
    return HELP_TEXT


@input_error
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = Record(name, phone)
    ADDRESSBOOK.add_record(rec)


@input_error
def change(*args):
    # for phone in self.phones:
    #     if old_phone == phone.value:
    #         self.phones.remove(phone)
    #         self.phones.append(Phone(new_phone))
    pass


# @input_error
# def delete_all(*args):
#     self.phones = list()

# @input_error
# def delete_this(*args):
#     for phone in self.phones:
#         if phone_number == phone.value:
#             self.phones.remove(phone)


# @input_error
def show_all(*args):
    return ADDRESSBOOK.show_all_rec()


COMMANDS = {
    hello: ["hello", "hi"],
    show_all: ["show all"],
    # show_rec: ["phone"],
    add: ["add"],
    change: ["change"],
    # remove_record: ["delete contact"],
    help_user: ["help"],
    bye: [".", "bye", "good bye", "close", "exit"],
}


def parse_command(text: str):
    for comm, key_words in COMMANDS.items():
        for key_word in key_words:
            if text.startswith(key_word):
                return comm, text.replace(key_word, "").strip().split(" ")
    return None, None


# Функція спілкування з юзером і виконання функцій відповідно до команди
def run_bot(user_input):
    command, data = parse_command(user_input)
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

    name = Name("Bill")
    phone = Phone("1234567890")
    rec = Record(name, phone)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab["Bill"], Record)
    assert isinstance(ab["Bill"].name, Name)
    assert isinstance(ab["Bill"].phones, list)
    assert isinstance(ab["Bill"].phones[0], Phone)
    assert ab["Bill"].phones[0].value == "1234567890"

    print("All Ok)")

    main()
