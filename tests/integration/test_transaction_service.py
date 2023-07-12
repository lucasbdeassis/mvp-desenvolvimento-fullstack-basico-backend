import unittest
from datetime import datetime
from uuid import uuid4

from src.adapters.transaction_repository import TransactionRepository
from src.application.transaction_service import TransactionService
from src.domain.transaction import Transaction
from src.infra.db import db_connection
from src.views.transaction_schema import (
    TransactionCreateSchema,
    TransactionUpdateSchema,
)


class TestTransactionService(unittest.TestCase):
    def test_create_transaction(self):
        transaction_create = TransactionCreateSchema(
            amount=10.0,
            description="test",
            category="test",
            date=datetime.now(),
        )  # type: ignore
        with db_connection() as conn:
            transaction_repository = TransactionRepository(conn)
            transaction_service = TransactionService(transaction_repository)
            result = transaction_service.create_transaction(transaction_create)
        assert isinstance(result, Transaction)

    def test_list_transaction(self):
        with db_connection() as conn:
            transaction_repository = TransactionRepository(conn)
            transaction_service = TransactionService(transaction_repository)
            result = transaction_service.list_transaction()
        assert isinstance(result, list)

    def test_get_transaction(self):
        with db_connection() as conn:
            transaction_repository = TransactionRepository(conn)
            transaction_service = TransactionService(transaction_repository)
            transaction_id = transaction_service.list_transaction()[0].id
            result = transaction_service.get_transaction(transaction_id)
        assert isinstance(result, Transaction)

    def test_update_transaction(self):
        with db_connection() as conn:
            transaction_repository = TransactionRepository(conn)
            transaction_service = TransactionService(transaction_repository)
            transaction_id = transaction_service.list_transaction()[0].id
            transaction_original = transaction_service.get_transaction(transaction_id)
            transaction_update = TransactionUpdateSchema(
                amount=transaction_original.amount + 30.0
            )  # type: ignore
            result = transaction_service.update_transaction(
                transaction_id, transaction_update
            )
        assert isinstance(result, Transaction)
        assert result != transaction_original
