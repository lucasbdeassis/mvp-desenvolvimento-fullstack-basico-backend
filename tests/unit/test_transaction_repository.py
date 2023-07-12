import unittest
from datetime import datetime
from uuid import uuid4

from src.adapters.transaction_repository import TransactionRepository
from src.domain.transaction import Transaction
from src.infra.db import engine


class TestTransactionRepository(unittest.TestCase):
    def setUp(self):
        self._connection = engine.connect()
        self._transaction_repository = TransactionRepository(self._connection)
        self._transaction = Transaction(
            id=uuid4(),
            amount=10.0,
            description="test",
            category="test",
            date=datetime.now(),
        )

    def tearDown(self):
        self._connection.close()

    def test_create(self):
        self._transaction_repository.create(self._transaction)
        transaction = self._transaction_repository.get(self._transaction.id)
        assert type(transaction) == Transaction
        assert transaction == self._transaction

    def test_get(self):
        self._transaction_repository.create(self._transaction)
        transaction = self._transaction_repository.get(self._transaction.id)
        assert type(transaction) == Transaction
        assert transaction == self._transaction

    def test_list(self):
        transactions = self._transaction_repository.list()
        assert type(transactions) == list

    def test_delete(self):
        self._transaction_repository.create(self._transaction)
        self._transaction_repository.delete(self._transaction.id)
        assert self._transaction_repository.get(self._transaction.id) is None

    def test_update(self):
        self._transaction_repository.create(self._transaction)
        updated_transaction = Transaction(**self._transaction.dict())
        updated_transaction.amount = 20.0
        self._transaction_repository.update(updated_transaction)
        transaction_ = self._transaction_repository.get(self._transaction.id)
        assert type(transaction_) == Transaction
        assert transaction_.amount == 20.0
