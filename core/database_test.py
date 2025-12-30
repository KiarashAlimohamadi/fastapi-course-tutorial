#--------------IMPORTS---------------------------------------------------

from sqlalchemy import create_engine,Column,Integer,String,Boolean
from sqlalchemy.orm import sessionmaker,declarative_base

#-------------------------------------------------------------------------


#--------------ُSTARTING DATABASE---------------------------------------------------



SQLALCHEMY_DATABASE_URL = "sqlite:///../sqlite.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

"""
create base class for declaring tables
"""
Base = declarative_base()

#---------------------------------------------------------------------------------


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30),nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean,default=True)
    is_verified = Column(Boolean,default=False)


    def __repr__(self):
        return f"User{self.id},first name{self.first_name},last name{self.last_name}"


"""
to create tables of the database
"""
Base.metadata.create_all(engine)
