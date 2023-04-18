from dataclasses import dataclass, field
from threading import Lock
from typing import Protocol
from uuid import UUID, uuid4


class ThreadSafeIdentifiable(Protocol):
    id: UUID
    lock: Lock


class HashableModel(ThreadSafeIdentifiable):
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: object):
        if hasattr(other, "id"):
            if isinstance(other.id, UUID):
                return self.id == other.id
        return NotImplemented


@dataclass(eq=False)
class Account(HashableModel):
    owner_id: UUID
    id: UUID = field(default_factory=uuid4)
    balance: float = 0.0
    active: bool = True
    lock: Lock = Lock()


@dataclass(eq=False)
class User(HashableModel):
    # list of unique ids for accounts held
    accounts: list[UUID] = field(default_factory=list)
    # unique identifier for the user
    id: UUID = uuid4()
    lock: Lock = Lock()
