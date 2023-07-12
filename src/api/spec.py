import json
from typing import Type, TypeVar

from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, render_template
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

SCHEMAS = dict()


# def add_schema(schema: Type[T]):
#     def decorator(func):
#         func.schema = schema
#         return func

#     return decorator


def add_schema(schemas: list[Type[T]]):
    for schema in schemas:
        SCHEMAS[schema.__name__] = schema.schema()


def config_spec(app: Flask):
    """
    Configura o módulo apispec para gerar a documentação da API no formato openapi.

    Uma cópia do arquivo openapi.json  é salva na pasta dos arquivo estaticos para
    disponibilização via o endpoint api/docs com o swagger UI.
    """

    spec = APISpec(
        title="Teste",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="Teste"),
        plugins=[FlaskPlugin()],
    )

    schemas = dict()

    with app.test_request_context():
        for view_name, view in app.view_functions.items():
            if view_name != "static":
                spec.path(view=view)
                # if hasattr(view, "schema"):
                #     schemas[view.schema.__name__] = view.schema.schema()

    for schema_name, schema in SCHEMAS.items():
        spec.components.schema(schema_name, schema)

    with open("src/api/static/openapi.json", "w") as f:
        json.dump(spec.to_dict(), f, indent=2, sort_keys=True)

    @app.route("/")
    def get_docs():
        return render_template("swaggerui.html")
