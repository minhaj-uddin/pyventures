from bank_system import BankSystem


class ATMController:
    def __init__(self):
        self.bank_system = BankSystem()
        self.current_user = None

    def register(self):
        print("\n--- User Registration ---")
        while True:
            account_number = input("Choose an account number: ")
            if account_number in self.bank_system.users:
                print("Account already exists. Try another.")
            else:
                break

        while True:
            pin = input("Set a 4-digit PIN: ")
            if len(pin) == 4 and pin.isdigit():
                break
            print("Invalid PIN. Must be 4 digits.")

        self.bank_system.create_account(account_number, pin)
        print(f"Account {account_number} created successfully.\n")

    def login(self):
        print("\n--- User Login ---")
        for _ in range(3):
            account_number = input('Enter account number: ')
            pin = input('Enter your 4-digit PIN: ')
            user = self.bank_system.authenticate(account_number, pin)
            if user:
                self.current_user = user
                print(f'\nWelcome, account {account_number}!\n')
                return True
            print('Invalid credentials.\n')

        print('Too many failed attempts. Exiting login.')
        return False

    def display_menu(self):
        print('\nATM Menu:')
        print('1. Check Balance')
        print('2. Deposit')
        print('3. Withdraw')
        print('4. View Transaction History')
        print('5. Logout')

    def get_number(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print('Please enter a valid number.')

    def check_balance(self):
        balance = self.current_user.get_balance()
        print(f'Your current balance is: ${balance:.2f}')

    def deposit(self):
        while True:
            try:
                amount = self.get_number('Enter deposit amount: ')
                self.current_user.deposit(amount)
                self.bank_system.save_users()
                print(f'Deposited ${amount:.2f} successfully.')
                break
            except ValueError as error:
                print(error)

    def withdraw(self):
        while True:
            try:
                amount = self.get_number('Enter withdrawal amount: ')
                self.current_user.withdraw(amount)
                self.bank_system.save_users()
                print(f'Withdrew ${amount:.2f} successfully.')
                break
            except ValueError as error:
                print(error)

    def view_transaction_history(self):
        history = self.current_user.get_transaction_history()
        if not history:
            print("No transactions found.")
        else:
            print("\nTransaction History:")
            for tx in history:
                print(f"{tx['time']} - {tx['type']}: ${tx['amount']:.2f}")

    def user_session(self):
        while True:
            self.display_menu()
            choice = input('Choose an option: ')
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.view_transaction_history()
            elif choice == '5':
                print('Logging out...\n')
                break
            else:
                print('Invalid option. Try again.')

    def run(self):
        while True:
            print("\nWelcome to the ATM System")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Select an option: ")
            if choice == '1':
                if self.login():
                    self.user_session()
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("Exiting system.")
                break
            else:
                print("Invalid option.")
