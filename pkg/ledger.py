from uuid import UUID

from pkg.models import Account, User
from pkg.record import Record


class AccountLedger(Record[Account]):
    def __init__(self):
        super().__init__(Account)

    def create(self, owner_id: UUID) -> UUID:
        return super().create(owner_id)


class UserLedger(Record[User]):
    def __init__(self):
        super().__init__(User)
