from assistant import *


def main():

    while True:
        user_input = str(input(">>>> "))
        result = run_bot(user_input)
        if result == 'Bye':
            print('Goodbye!')
            break
        print(result)


if __name__ == "__main__":
    main()