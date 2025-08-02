class Denomination:
    def __init__(self, value: str, count: int = 0):
        self.value = value
        self.count = count

def total_value(self):
    return self.value * self.count

""" 
User, Card, and Account 
"""

class Account:
    def __init__(self, account_number: int, balance: float):
        self.account_number = account_number
        self.balance = balance
    
    def deposit(self, amount: int):
        self.balance += amount

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise Exception("Insufficient funds in account.")
        self.balance -= amount


class Card:
    def __init__(self, card_number: str, pin: int, account: Account):
        self.card_number = card_number
        self.pin = pin
        self.account = account
    

class User:
    def __init__(self, name: str, card: Card):
        self.name = name
        self.card = card


"""
Transaction (Abstract + Subclasses)
Using Inheritance + Strategy Pattern 
"""
from abc import ABC, abstractmethod
from typing import List

class Transaction(ABC):
    @abstractmethod
    def execute(self, atm: 'ATM', card: Card):
        pass


class BalanceCheck(Transaction):
    def execute(self, atm: 'ATM', card: Card):
        print(f"Balance for account {card.account.account_number}: {card.account.balance}")
    

class Deposit(Transaction):
    def __init__(self, deposit_amount: float):
        self.deposit_amount = deposit_amount

    def execute(self, atm: 'ATM', card: Card):
        card.account.deposit(self.deposit_amount)
        atm.deposit_cash(self.deposit_amount)  # Update ATM cash
        print("Deposit successful.")
    

class Withdrawal(Transaction):
    def __init__(self, withdraw_amount: float):
        self.withdraw_amount = withdraw_amount

    def execute(self, atm: 'ATM', card: Card):
        if not atm.can_dispense(self.withdraw_amount):
            raise Exception("ATM cannot dispense the requested amount.")
        card.account.withdraw(self.withdraw_amount)
        atm.dispense_cash(self.withdraw_amount)
        print("Withdrawal successful.")


# CashInventory

class CashInventory:
    def __init__(self):
        self.denominations = {
            2000: Denomination(2000, 10),
            1000: Denomination(1000, 20),
            500: Denomination(500, 50)
        }

    def total_cash(self):
        return sum(d.total_value() for d in self.denominations)
    
    def can_dispense_amount(self, amount: int) -> bool:
        # Simplified greedy algorithm
        temp_amount = amount
        for note_value in sorted(self.denominations.keys(), reverse=True):
            count = min(temp_amount // note_value, self.denominations[note_value].count)
            temp_amount -= count * note_value
        return temp_amount == 0
    
    def dispense_amount(self, amount: int) -> dict:
        if not self.can_dispense_amount(amount):
            raise Exception("Cannot dispense this amount with available denominations.")
        
        result = {}

        for note_value in sorted(self.denominations.keys(), reverse=True):
            count = min(amount // note_value, self.denominations[note_value].count)
            if count > 0:
                self.denominations[note_value].count -= count
                result[note_value] = count
                amount -= count * note_value

        return result
    
    def deposit_amount(self, amount: int):
        # Assume all deposits are in 500s for simplicity
        self.denominations[500].count += amount // 500


class ATM:
    def __init__(self):
        self.cash_inventory = CashInventory()
        self.current_card: Card | None = None

    def insert_card(self, card: Card, pin: int):
        if card.pin != pin:
            raise Exception("Invalid PIN.")
        self.current_card = card
        print("Card authenticated.")
    
    def execute_transaction(self, transaction: Transaction):
        if not self.current_card:
            raise Exception("Insert card first.")
        transaction.execute(self, self.current_card)

    def can_dispense(self, amount: int) -> bool:
        return self.cash_inventory.can_dispense_amount(amount) 
    
    def dispense_cash(self, amount: int):
        breakdown = self.cash_inventory.dispense_amount(amount)
        print(f"Dispensed: {breakdown}")
    
    def deposit_cash(self, amount: int):
        self.cash_inventory.deposit_amount(amount)

    def eject_card(self):
        self.current_card = None
        print("Card ejected.")


def test_ATM():
    account = Account('123456', 5000)
    card = Card('892-3834', 1234, account)
    user = User('Prateek', card)

    atm = ATM()

    # atm.insert_card(card, 3455)

    atm.insert_card(card, 1234)
    atm.execute_transaction(BalanceCheck())
    # atm.execute_transaction(Withdrawal(2300))
    atm.execute_transaction(Deposit(1000))
    atm.execute_transaction(BalanceCheck())
    atm.execute_transaction(Withdrawal(2500))
    atm.eject_card()


if __name__ == "__main__":
    test_ATM()