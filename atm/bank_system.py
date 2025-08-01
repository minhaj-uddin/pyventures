import os
import json
from account import UserAccount, hash_pin


class BankSystem:
    def __init__(self, data_file='users.json'):
        self.users = {}
        self.data_file = data_file
        self.load_users()

    def load_users(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for user_data in data.values():
                    user = UserAccount.from_dict(user_data)
                    self.users[user.account_number] = user

    def save_users(self):
        data = {acc: user.to_dict() for acc, user in self.users.items()}
        with open(self.data_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def create_account(self, account_number, pin):
        if account_number in self.users:
            raise ValueError('Account already exists.')
        hashed = hash_pin(pin)
        self.users[account_number] = UserAccount(account_number, hashed)
        self.save_users()

    def authenticate(self, account_number, pin):
        user = self.users.get(account_number)
        if user and user.check_pin(pin):
            return user
        return None
