from sqlalchemy import Column, Integer, String, Table, Engine
from sqlalchemy.orm import declarative_base

db = declarative_base()


def create_all(engine: Engine):
    db.metadata.create_all(bind=engine)


class Password(db.Model):
    __tablename__ = "pwdata"

    id = Column(Integer, primary_key=True)
    site = Column(String(256))
    pw = Column(String(256))
