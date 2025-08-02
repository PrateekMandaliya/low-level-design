# Functional Requirements

1. A customer can:

- Insert card and authenticate using a PIN
- View balance
- Deposit cash
- Withdraw cash (with denomination breakdown)
- View mini statement

2. The ATM should:

- Check if sufficient funds are available (in account and machine)
- Dispense denominations based on availability
- Accept cash deposits in accepted denominations only

# Non-Functional Requirements

1. Concurrency-safe operations
2. Extensible to support new denominations
3. Maintain logs of transactions
4. Support multiple ATMs (for scalability)

# Actors and Classes of System

Customer – Initiates transactions.
ATM Machine – Interface to the system.
Bank System – Holds account information.
Cash Dispenser – Physical dispenser in ATM.
Deposit Slot – Accepts and validates deposits.
