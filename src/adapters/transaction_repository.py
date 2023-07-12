import json
from datetime import datetime
from uuid import UUID

from sqlalchemy import Connection, text

from src.adapters.abc_repository import AbstractRepository
from src.domain.transaction import Transaction


class TransactionRepository(AbstractRepository):
    def __init__(self, connection: Connection):
        self.connection = connection

    def create(self, transaction: Transaction):
        query = text(
            """--sql
            INSERT INTO 
                "transaction" (
                    id, 
                    amount, 
                    description, 
                    category, 
                    date,
                    tags,
                    created_at, 
                    updated_at
                )
            VALUES (
                    :id, 
                    :amount, 
                    :description, 
                    :category, 
                    :date,
                    :tags,
                    :created_at, 
                    :updated_at
                )
        """
        )

        params = transaction.dict()

        params["id"] = str(params["id"])
        params["tags"] = json.dumps(params["tags"])

        self.connection.execute(query, params)

    def get(self, id: UUID) -> Transaction | None:
        query = text(
            """--sql
            SELECT 
                * 
            FROM 
                "transaction" 
            WHERE 
                id = :id
        """
        )

        id = str(id)  # type: ignore

        rs = self.connection.execute(query, {"id": id}).mappings().first()

        if rs:
            data = dict(rs)
            data["tags"] = json.loads(data["tags"])
            return Transaction(**data)

    def update(self, transaction: Transaction):
        query = text(
            """--sql
            UPDATE 
                "transaction" 
            SET 
                amount = :amount, 
                description = :description, 
                category = :category, 
                date = :date,
                tags = :tags,
                updated_at = :updated_at
            WHERE
                id = :id
        """
        )

        params = transaction.dict()

        params["id"] = str(params["id"])
        params["tags"] = json.dumps(params["tags"])
        params["updated_at"] = datetime.now()

        self.connection.execute(query, params)

    def delete(self, id: UUID):
        query = text(
            """--sql
            DELETE FROM
                "transaction"
            WHERE
                id = :id
        """
        )

        id = str(id)  # type: ignore

        self.connection.execute(query, {"id": id})

    def list(self) -> list[Transaction]:
        query = text(
            """--sql
            SELECT 
                * 
            FROM 
                "transaction"
        """
        )

        rs = self.connection.execute(query).mappings().all()

        transaction_list = []

        for row in rs:
            data = dict(row)
            data["tags"] = json.loads(data["tags"])
            transaction_list.append(Transaction(**data))

        return transaction_list
