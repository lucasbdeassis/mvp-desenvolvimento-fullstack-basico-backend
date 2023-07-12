import unittest
from unittest.mock import Mock
from uuid import uuid4

from src.application.transaction_service import TransactionService
from src.domain.transaction import Transaction
from tests.fakes.fake_repository import FakeRepository


class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self._transaction_repository = FakeRepository()
        self._transaction_service = TransactionService(self._transaction_repository)

    def test_create_transaction(self):
        transaction = Transaction(
            id=uuid4(),
            amount=10.0,
            description="test",
            category="test",
            date="2022-01-01",
        )
        self._transaction_repository.create.return_value = transaction
        result = self._transaction_service.create_transaction(transaction)
        self.assertEqual(result, transaction)

    def test_get_transaction(self):
        transaction = Transaction(
            id=uuid4(),
            amount=10.0,
            description="test",
            category="test",
            date="2022-01-01",
        )
        self._transaction_repository.get.return_value = transaction
        result = self._transaction_service.get_transaction("123")
        self.assertEqual(result, transaction)

    def test_list_transactions(self):
        transactions = [
            Transaction(
                id=uuid4(),
                amount=10.0,
                description="test",
                category="test",
                date="2022-01-01",
            ),
            Transaction(
                id="456",
                amount=20.0,
                description="test2",
                category="test2",
                date="2022-01-02",
            ),
        ]
        self._transaction_repository.list.return_value = transactions
        result = self._transaction_service.list_transactions()
        self.assertEqual(result, transactions)

    def test_delete_transaction(self):
        self._transaction_service.delete_transaction("123")
        self._transaction_repository.delete.assert_called_once_with("123")

    def test_update_transaction(self):
        transaction = Transaction(
            id=uuid4(),
            amount=10.0,
            description="test",
            category="test",
            date="2022-01-01",
        )
        self._transaction_service.update_transaction(transaction)
        self._transaction_repository.update.assert_called_once_with(transaction)
