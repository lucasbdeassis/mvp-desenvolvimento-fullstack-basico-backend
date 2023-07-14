from uuid import uuid4

from flask import Blueprint, request

from src.adapters.transaction_repository import TransactionRepository
from src.api.spec import add_schema
from src.application.transaction_service import TransactionService
from src.domain.transaction import Transaction
from src.infra.db import db_connection
from src.views.transaction_schema import (
    TransactionCreateSchema,
    TransactionSchema,
    TransactionUpdateSchema,
)

transaction_controller = Blueprint("transaction_controller", __name__)

add_schema([TransactionCreateSchema, TransactionSchema, TransactionUpdateSchema])


@transaction_controller.route("/transactions", methods=["POST"])
def create_transaction():
    """
    ---
    post:
      summary: Adds a new transaction
      description: Adds a new transaction
      requestBody:
        required: true
        content:
          application/json:
            schema: TransactionCreateSchema
      responses:
        200:
          description: the created transaction
          content:
            application/json:
              schema: TransactionCreateSchema
    """
    try:
        transaction_create = TransactionCreateSchema(**request.json)  # type: ignore
    except Exception as e:
        return {"error": str(e)}, 400
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transaction = service.create_transaction(transaction_create)
        return transaction.dict(), 201


@transaction_controller.route("/transactions/<id>", methods=["GET"])
def get_transaction(id):
    """
    ---
    get:
      summary: Returns a transaction
      description: Returns a transaction
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type : string
      responses:
        200:
          description: a transaction
          content:
            application/json:
              schema: TransactionSchema
        404:
          description: Transaction not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: Transaction not found
    """
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transaction = service.get_transaction(id)
        if not transaction:
            return {"error": "Transaction not found"}, 404
        return transaction.dict(), 200


@transaction_controller.route("/transactions", methods=["GET"])
def list_transaction():
    """
    ---
    get:
      summary: Returns a list of transactions
      description: Returns a list of transactions
      responses:
        200:
          description: list of transactions
          content:
            application/json:
              schema: TransactionSchema
    """
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transactions = service.list_transaction()
        return [transaction.dict() for transaction in transactions], 200


@transaction_controller.route("/transactions/<id>", methods=["DELETE"])
def delete_transaction(id):
    """
    ---
    delete:
      summary: Removes a transaction
      description: Removes a transaction
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type : string
      responses:
        200:
          description: success message
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: Transaction deleted successfully
        404:
          description: Transaction not found
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: Transaction not found
    """
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transaction = service.delete_transaction(id)
        if not transaction:
            return {"error": "Transaction not found"}, 404
        return {"message": "Transaction deleted successfully"}, 200
