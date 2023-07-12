from contextlib import contextmanager

from sqlalchemy import create_engine

db_url = "sqlite:///database.sqlite3"

engine = create_engine(db_url, echo=False)


@contextmanager
def db_connection():
    connection = engine.connect()
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.commit()
        connection.close()
