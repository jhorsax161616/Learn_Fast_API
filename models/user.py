from sqlalchemy import Integer, Table, Column, String
from config.db import meta, engine

users = Table("users", meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(180)),
    Column("email", String(180)),
    Column("pasword", String(180)))

meta.create_all(engine)