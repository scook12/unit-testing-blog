from uuid import uuid4


class Identifiable(object):
    def __init__(self, item_id):
        self.id = item_id


class LedgerMock:
    def __init__(self):
        self.items = []
        self.read_called = 0
        self.create_called = 0
        self.delete_called = 0

    def read(self, param):
        self.read_called += 1
        self.items.append(param)
        return Identifiable(param)

    def create(self, owner_id):
        self.create_called += 1
        o = Identifiable(uuid4())
        self.items.append(o.id)
        return o

    def delete(self, param):
        self.delete_called += 1


class MockAcct:
    def __init__(self, *args, **kwargs):
        self.active = kwargs.get('active', True)
        self._balance = kwargs.get('balance', 0)
        self.active_called = 0
        self.balance_called = 0
        self.set_balance_called = 0

    @property
    def balance(self):
        self.balance_called += 1
        return self._balance

    @balance.setter
    def balance(self, new_bal):
        self.set_balance_called += 1
        self._balance = new_bal

    def transact(self, *args, **kwargs):
        return self
