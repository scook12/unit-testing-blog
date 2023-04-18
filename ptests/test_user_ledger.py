from uuid import UUID, uuid4

import pytest

from pkg import ledger


@pytest.fixture
def user_ledger():
    records = ledger.UserLedger()
    yield records
    records.clear()


def test_create_user(user_ledger):
    user_id = user_ledger.create()
    assert isinstance(user_id, UUID)
    assert user_ledger.count == 1


def test_read_user(user_ledger):
    with pytest.raises(LookupError):
        user_ledger.read(uuid4())

    user_id = user_ledger.create()
    user = user_ledger.read(user_id)
    assert user.id == user_id
    assert len(user.accounts) == 0


def test_delete_user(user_ledger):
    with pytest.raises(LookupError):
        user_ledger.delete(uuid4())

    user_id = user_ledger.create()
    assert user_ledger.count == 1
    user_ledger.delete(user_id)
    assert user_ledger.count == 0

    with pytest.raises(LookupError):
        user_ledger.read(user_id)
