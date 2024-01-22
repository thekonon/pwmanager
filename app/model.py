from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .entity import create_all, Password
from pieceful import Piece

engine = create_engine("sqlite:///main.db")
session_local = sessionmaker(engine)


@Piece("model")
class Model:
    def __init__(self) -> None:
        create_all(engine)

    def save_password(self, site: str, password: str):
        pw = Password(site=site, pw=password)

        with session_local() as session:
            session.add(pw)
            session.commit()

    def get_password(self, site: str) -> str:
        with session_local() as session:
            pw = session.query(Password).filter(Password.site == site).first()
            if pw is None:
                raise ValueError(f"Site {site} is not in the database!")
            return str(pw.pw)

    def get_all_sites(self) -> list[str]:
        with session_local() as session:
            passwords = session.query(Password).filter(Password.site != "MAINPW").all()
            return [str(pw.site) for pw in passwords]
