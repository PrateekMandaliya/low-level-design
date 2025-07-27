"""
    STRATEGY DESIGN PATTERN

Imagine you have a single task that can be accomplished in multiple ways. 
Instead of cluttering your code with complex "if-else" or "switch" statements to handle these different approaches, 
the Strategy Design Pattern lets you "swap in" different ways of doing things at runtime. 
It essentially defines a family of interchangeable algorithms, encapsulates each one into 
a separate class (a "strategy"), and allows you to switch between them as needed.


"""

from abc import ABC, abstractmethod

# 1. Define the Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# 2. Create Concrete Strategy Classes
class CreditCardPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using Credit Card.")

class PayPalPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using PayPal.")

class BankTransferPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount} using Bank Transfer.")

# 3. Create the Context Class
class PaymentGateway:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def process_payment(self, amount):
        self._strategy.pay(amount)

# 4. Allow for Strategy Selection and Use
if __name__ == "__main__":
    # Client chooses a strategy
    credit_card_payment = CreditCardPayment()
    paypal_payment = PayPalPayment()
    bank_transfer_payment = BankTransferPayment()

    # Client sets the initial strategy for the context
    payment_context = PaymentGateway(credit_card_payment)
    payment_context.process_payment(100)  # Output: Paid 100 using Credit Card.

    # Client can change the strategy at runtime
    payment_context.set_strategy(paypal_payment)
    payment_context.process_payment(50)   # Output: Paid 50 using PayPal.

    payment_context.set_strategy(bank_transfer_payment)
    payment_context.process_payment(200)  # Output: Paid 200 using Bank Transfer.
