import os

from sqlalchemy import text

from src.infra.db import Session

session = Session()

sql_folder = "sql"
sql_files = [f for f in os.listdir(sql_folder) if f.endswith(".sql")]

for sql_file in sql_files:
    with open(os.path.join(sql_folder, sql_file), "r") as f:
        sql_script = f.read()
        session.execute(text(sql_script))

session.commit()
