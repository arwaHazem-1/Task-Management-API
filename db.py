from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///tasks.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    # No generator here, just a simple function
    session = Session(engine)
    return session
