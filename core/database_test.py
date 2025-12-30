from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./sqlite.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

"""
create base class for declaring tables
"""
Base = declarative_base()



"""
to create tables of the database
"""
Base.metadata.create_all(engine)
