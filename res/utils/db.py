from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData, LargeBinary
from sqlalchemy.orm import declarative_base, Session
from typing import List
from datetime import datetime

Base = declarative_base()

def current_date_time() -> str:
    now = datetime.now()
    formatted_date_time = now.strftime("%d.%m.%Y-%H:%M:%S")
    return formatted_date_time

class Password(Base):
    __table__ = Table('pwdata', Base.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('site', String),
                      Column('date', String),
                      Column('pw', LargeBinary))

class SessionManager():
    def __init__(self, engine) -> None:
        self.engine = engine
    def __enter__(self):
        self.session = Session(self.engine)
        return self.session
    def __exit__(self, *args):
        self.session.close()
    
    
class DBHandler:
    def __init__(self, database_url: str = 'sqlite:///main.db') -> None:
        """
        Initialize the DBHandler with the specified database URL.

        Args:
            database_url (str): The URL of the database (default is 'sqlite:///main.db').
        """
        self._engine = create_engine(database_url)
        Base.metadata.create_all(bind=self._engine)

    def _create_session(self):
        """
        Create a new session for database operations.

        Returns:
            Session: SQLAlchemy session object.
        """
        return Session(self._engine)

    def _close_session(self, session):
        """
        Close the given session.

        Args:
            session (Session): SQLAlchemy session object.
        """
        session.close()

    def save_password(self, site: str, password: bytes, date: str = current_date_time()):
        """
        Save a password for a specific site in the database.

        Args:
            site (str): The name of the site.
            password (bytes): The password to be saved.
        (Optional)
            date (str): Date of that password
        """
        with SessionManager(self._engine) as session:
            session.add_all([Password(site=site, pw=password, date = date)])
            session.commit()

    def get_password(self, site: str) -> bytes:
        """
        Retrieve the password for a specific site from the database.

        Args:
            site (str): The name of the site.

        Returns:
            bytes: The password bytes.
        
        Raises:
            ValueError: If the site is not found in the database.
        """
        with self._create_session() as session:
            pw_data = session.query(Password).filter(Password.site == site).first()
            if pw_data:
                return pw_data.pw
            else:
                raise ValueError("Site is not in the database!")

    def get_all_sites(self) -> List[str]:
        """
        Return a list of site names from the database - except MAINPW.

        Returns:
            List[str]: List of strings containing site names.
        """
        with self._create_session() as session:
            pw_data = session.query(Password).filter(Password.site != "MAINPW").all()
            return [data.site for data in pw_data]


if __name__ == '__main__':
    handle = DBHandler()
    handle.save_password("Main", "WAAA".encode())
    print(handle.get_password("Main"))
