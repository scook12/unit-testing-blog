import pytest
from uuid import uuid4
from pkg.teller import Teller
from mocks import LedgerMock, MockAcct
from unittest.mock import patch


@pytest.fixture
def teller():
    teller = Teller()
    yield teller


def test_close_account(teller):
    accounts = LedgerMock()
    mock_acct = MockAcct()
    with patch.object(teller, 'accounts', accounts):
        with patch.object(teller, '_transact', mock_acct.transact):
            user_id, account_id = uuid4(), uuid4()
            teller.close_account(user_id, account_id)
            assert accounts.delete_called == 1


def test_create_account(teller):
    user_id = uuid4()
    accounts = LedgerMock()
    users = LedgerMock()
    with patch.object(teller, 'accounts', accounts):
        with patch.object(teller, 'users', users):
            teller.create_account(user_id)
            assert users.read_called == 1
            assert accounts.create_called == 1


def test_get_balance(teller):
    mock_acct = MockAcct()
    with patch.object(teller, '_transact', mock_acct.transact):
        bal = teller.get_balance(uuid4(), uuid4())
        assert bal == 0
        assert mock_acct.balance_called == 1


def test_deposit(teller):
    mock_acct = MockAcct()
    with patch.object(teller, '_transact', mock_acct.transact):
        user_id, acct_id = uuid4(), uuid4()
        teller.deposit(user_id, acct_id, 20)
        assert mock_acct.set_balance_called == 1
        assert mock_acct.balance == 20

        with pytest.raises(ValueError):
            teller.deposit(user_id, acct_id, 0)


def test_withdrawal(teller):
    mock_account = MockAcct(balance=20)
    with patch.object(teller, '_transact', mock_account.transact):
        user_id, acct_id = uuid4(), uuid4()
        teller.withdrawal(user_id, acct_id, 15)
        assert mock_account.balance_called == 2
        assert mock_account.set_balance_called == 1
        assert mock_account.balance == 5

        with pytest.raises(ValueError):
            teller.withdrawal(user_id, acct_id, 0)

        with pytest.raises(ValueError):
            teller.withdrawal(user_id, acct_id, 2500)
