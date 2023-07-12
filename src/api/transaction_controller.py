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
def create():
    """
    ---
    post:
      summary: Adiciona uma nova transação
      description: Adiciona uma nova transação
      requestBody:
        required: true
        content:
          application/json:
            schema: TransactionCreateSchema
      responses:
        200:
          description: Retorna a transação criada
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
def get(id):
    """
    ---
    get:
      summary: Retorna uma transação por id
      description: Retorna uma transação por id
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type : string
      responses:
        200:
          description: Retorna o tenant criado
          content:
            application/json:
              schema: TransactionSchema
    """
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transaction = service.get_transaction(id)
        return transaction.dict(), 200


@transaction_controller.route("/transactions", methods=["GET"])
def list_transaction():
    """
    ---
    get:
      summary: Retorna uma lista de transações
      description: Retorna uma lista de transações
      responses:
        200:
          description: Retorna o tenant criado
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
def delete(id):
    """
    ---
    delete:
      summary: Remove uma transação
      description: Remove uma transação
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type : string
      responses:
        200:
          description: Retorna o tenant criado
          content:
            application/json:
              schema: TransactionSchema
    """
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        service.delete_transaction(id)
        return {"message": "Transaction deleted successfully"}, 200


@transaction_controller.route("/transactions/<id>/tags", methods=["POST"])
def add_tags(id):
    """
    ---
    post:
      summary: Adiciona uma nova tag
      description: Adiciona uma nova tag
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type : string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                type: string
      responses:
        200:
          description: Retorna a transação editada
          content:
            application/json:
              schema: TransactionCreateSchema
    """
    tags = request.json
    if not isinstance(tags, list):
        return {"error": "Tags must be a list"}, 400
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transaction = service.add_tags(id, tags)
        return transaction.dict(), 200


@transaction_controller.route("/transactions/<id>/tags", methods=["DELETE"])
def remove_tags(id):
    """
    ---
    post:
      summary: Remove uma tag
      description: Remove uma tag
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type : string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: array
              items:
                type: string
      responses:
        200:
          description: Retorna a transação editada
          content:
            application/json:
              schema: TransactionCreateSchema
    """
    tags = request.json
    if not isinstance(tags, list):
        return {"error": "Tags must be a list"}, 400
    with db_connection() as session:
        repository = TransactionRepository(session)
        service = TransactionService(repository)
        transaction = service.remove_tags(id, tags)
        return transaction.dict(), 200


# @transaction_controller.route("/transaction/tags", methods=["GET"])
# def list_trasactions_by_tag():
#     with db_connection() as session:
#         repository = TransactionRepository(session)
#         service = TransactionService(repository)
#         transactions = service.list_by_tag(request.args["tag"])
#         return [transaction.dict() for transaction in transactions], 200
