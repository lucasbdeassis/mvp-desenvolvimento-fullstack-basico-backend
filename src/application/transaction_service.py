from uuid import uuid4

from src.adapters.abc_repository import AbstractRepository
from src.domain.transaction import Transaction
from src.views.transaction_schema import (
    TransactionCreateSchema,
    TransactionUpdateSchema,
)


class TransactionService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def create_transaction(self, transaction_create: TransactionCreateSchema):
        transaction = Transaction(**transaction_create.dict(), id=uuid4())
        self.repository.create(transaction)
        return transaction

    def get_transaction(self, id) -> Transaction:
        transaction: Transaction = self.repository.get(id)
        return transaction

    def list_transaction(self) -> list[Transaction]:
        return self.repository.list()

    def delete_transaction(self, id):
        transaction = self.repository.get(id)
        if not transaction:
            return None
        return transaction

    def add_tags(self, id: str, tags: list[str]):
        transaction: Transaction = self.repository.get(id)
        transaction.add_tags(tags)
        self.repository.update(transaction)
        return transaction

    def remove_tags(self, id: str, tags: list[str]):
        transaction: Transaction = self.repository.get(id)
        transaction.remove_tags(tags)
        self.repository.update(transaction)
        return transaction

    def update_transaction(
        self, id, transaction_update: TransactionUpdateSchema
    ) -> Transaction | None:
        transaction: Transaction = self.repository.get(id)
        if not transaction:
            return None
        transaction_data = transaction.dict()
        update_data = transaction_update.dict(exclude_unset=True)
        updated_transaction = Transaction(**{**transaction_data, **update_data})
        updated_transaction.id = id
        self.repository.update(updated_transaction)
        return updated_transaction
