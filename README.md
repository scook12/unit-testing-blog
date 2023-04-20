# unit testing blog code

TODO:
- [x] pytest examples
- [x] mocking examples
- [ ] doctest examples
- [x] tox config
- [x] travis config
- [ ] hypo testing
- [ ] integration test - maybe store account data in a db or add the Teller class

# Design

## Models

### Account
### User


## Ledgers (Database)

This is a Singleton record-keeping object that maintains a set of all accounts held or users registered.
It initializes the account/user itself and generates their unique ids. Since it stores all records,
it's also responsible for retrieving existing objects.

## Teller (Server)

This is the controller for the records. Its responsibility is to validate and route user requests for transactions.
There can be an infinite number of tellers.

## Client (Client)

A client is responsible for making requests to the Teller.
There can be infinite number of clients. This isn't a defined object in the API.

## Data flows

### New account
- Client requests new account from teller
- Teller requests user from ledger
  - If no user, Teller initializes new User
- Teller requests new account using Ledger
- Ledger stores new account

### Transaction
- Client requests new transaction from teller for User
- Teller seeks existing account using Ledger
  - If no account, Teller rejects
  - If account specified is not owned by User, Teller rejects
  - If valid account target, Ledger returns account
- Teller validates transaction request against account
  - If transaction request invalid, Teller rejects
- Teller requests transaction
- Account executes transaction request

### Close account
- Client requests account be closed for User
- Teller seeks existing user using Ledger
  - If no user, Teller rejects
- Teller seeks existing account using Ledger
  - If no account, Teller rejects
  - If account specified is not owned by User, Teller rejects
  - If valid account target, Ledger returns account
- Teller requests close operation from account
- Account executes close
- Teller requests delete operation from ledger
- Teller executes delete

### Delete user
- Client requests User be deleted
- Teller seeks existing user using Ledger
  - If no user, Teller rejects
- Teller requests delete operation from ledger
- Teller executes delete
  - All accounts closed and removed from ledger
  - User record deleted

As a prerequisite to all transactions, Client initializes "connection" by instantiating a Teller.


# The testing

