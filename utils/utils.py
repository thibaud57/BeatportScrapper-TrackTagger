def get_user_input():
    while True:
        user_input = input("Replace this file? (Y/N) ").lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print("Invalid input. Please enter Y or N.")


def clean_string(s):
    return s.replace('_', ' ')


def clean_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename
