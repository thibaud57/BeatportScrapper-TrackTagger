def get_user_input():
    while True:
        user_input = input("Replace this file? (Y/N) ").lower()
        if user_input in ['y', 'n']:
            return user_input
        else:
            print("Invalid input. Please enter Y or N.")
