from __future__ import annotations

from threading import Lock
from typing import Generic, Type, TypeVar
from uuid import UUID

from pkg.models import ThreadSafeIdentifiable

T = TypeVar("T", bound=ThreadSafeIdentifiable)


class Record(Generic[T]):
    """
    Generic Singleton bookkeeper CRD API.
    Designed explicitly for single inheritance.
    """

    __instance = None
    _items: set[T] = set()
    __lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Record, cls).__new__(cls)
        return cls.__instance

    def __init__(self, record_type: Type[T]):
        self._type = record_type

    def __get(self: Record[T], item_id: UUID) -> T:
        try:
            item = next(filter(lambda i: i.id == item_id, self._items))
        except StopIteration:
            raise LookupError
        return item

    def __remove(self, item_id: UUID) -> None:
        item: T = self.__get(item_id)
        with item.lock:
            self._items.remove(item)

    @property
    def count(self):
        return len(self._items)

    def read(self, item_id: UUID) -> T:
        return self.__get(item_id)

    def create(self, *args, **kwargs) -> UUID:
        item: T = self._type(*args, **kwargs)
        self._items.add(item)
        return item.id

    def delete(self, item_id: UUID) -> UUID:
        self.__remove(item_id)
        return item_id

    def clear(self):
        self._items.clear()
