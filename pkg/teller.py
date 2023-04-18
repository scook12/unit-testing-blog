from uuid import UUID

from pkg.ledger import AccountLedger, UserLedger
from pkg.models import Account


class Teller:
    def __init__(self):
        self.users = UserLedger()
        self.accounts = AccountLedger()

    def _transact(
        self, user_id: UUID, account_id: UUID, active: bool = True
    ) -> Account:
        user = self.users.read(user_id)  # user exists
        acct = self.accounts.read(account_id)  # acct exists
        if acct.id not in user.accounts:
            raise ValueError
        if active:
            # account active
            if not acct.active:
                raise ValueError
        return acct

    def get_balance(self, user_id: UUID, account_id: UUID):
        account = self._transact(user_id, account_id)
        return account.balance

    def create_account(self, user_id: UUID):
        try:
            user = self.users.read(user_id)
        except LookupError:
            user_id = self.users.create()
            user = self.users.read(user_id)
        self.accounts.create(user.id)

    def close_account(self, user_id: UUID, account_id: UUID):
        self._transact(user_id, account_id)
        self.accounts.delete(account_id)

    def deposit(self, user_id: UUID, account_id: UUID, amount: float):
        if not amount > 0:
            raise ValueError  # noop
        acct = self._transact(user_id, account_id)
        acct.balance += amount

    def withdrawal(self, user_id: UUID, account_id: UUID, amount: float):
        if not amount > 0:
            raise ValueError  # noop
        acct = self._transact(user_id, account_id)
        if not acct.balance > amount:
            raise ValueError  # overdraft

        # in pure design world, the update op
        # should be handled by the ledger, but it's
        # nonsense since we've already retrieved the account
        acct.balance -= amount

    def purge(self, user_id: UUID):
        user = self.users.read(user_id)
        for acct in user.accounts:
            self.accounts.delete(acct)
        self.users.delete(user.id)
