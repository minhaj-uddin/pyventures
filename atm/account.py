import hashlib
from datetime import datetime


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


class UserAccount:
    def __init__(self, account_number, hashed_pin, balance=0, transaction_history=None):
        self.account_number = account_number
        self._hashed_pin = hashed_pin
        self.balance = balance
        self.transaction_history = transaction_history or []

    def check_pin(self, input_pin):
        return hash_pin(input_pin) == self._hashed_pin

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError('Deposit amount must be positive.')
        self.balance += amount
        self._add_transaction('Deposit', amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError('Withdrawal amount must be positive.')
        if amount > self.balance:
            raise ValueError('Insufficient funds.')
        self.balance -= amount
        self._add_transaction('Withdrawal', amount)

    def _add_transaction(self, transaction_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append({
            'type': transaction_type,
            'amount': amount,
            'time': timestamp
        })

    def get_transaction_history(self):
        return self.transaction_history

    def get_balance(self):
        return self.balance

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'pin': self._hashed_pin,
            'balance': self.balance,
            'transaction_history': self.transaction_history
        }

    @staticmethod
    def from_dict(data):
        return UserAccount(
            data['account_number'],
            data['pin'],
            data['balance'],
            data.get('transaction_history', [])
        )
