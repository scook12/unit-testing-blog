from uuid import UUID, uuid4

import pytest

from pkg import ledger


@pytest.fixture
def account_ledger():
    records = ledger.AccountLedger()
    yield records
    records.clear()


def test_create_account(account_ledger):
    owner_id = uuid4()
    acct_id = account_ledger.create(owner_id)

    assert isinstance(acct_id, UUID)
    assert account_ledger.count == 1


def test_read_account(account_ledger):
    with pytest.raises(LookupError):
        account_ledger.read(uuid4())

    owner_id = uuid4()
    acct_id = account_ledger.create(owner_id)
    account = account_ledger.read(acct_id)

    assert account.id == acct_id
    assert account.active
    assert account.balance == 0
    assert account.owner_id == owner_id


def test_delete_account(account_ledger):
    with pytest.raises(LookupError):
        account_ledger.delete(uuid4())

    owner_id = uuid4()
    acct_id = account_ledger.create(owner_id)
    assert account_ledger.count == 1
    account_ledger.delete(acct_id)
    assert account_ledger.count == 0
    with pytest.raises(LookupError):
        account_ledger.read(acct_id)
