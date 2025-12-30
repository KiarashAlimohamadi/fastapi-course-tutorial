#--------------IMPORTS---------------------------------------------------

from sqlalchemy import create_engine,Column,Integer,String,Boolean,ForeignKey,Table,UniqueConstraint
from sqlalchemy.orm import sessionmaker,declarative_base,relationship

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

enrollments = Table("enrollments",Base.metadata,
                    Column("id",Integer,primary_key=True,autoincrement=True),
                    Column("user_id",Integer,ForeignKey("users.id")),
                    Column("address_id",Integer,ForeignKey("addresses.id")),
                    UniqueConstraint("user_id","address_id",name="unique_user_course_enrolled")
                    )



class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30),nullable=True)
    age = Column(Integer)
    is_active = Column(Boolean,default=True)
    is_verified = Column(Boolean,default=False)

    addresses = relationship("Address",back_populates="user",secondary=enrollments)

    def __repr__(self):
        return f"User{self.id},first name : {self.first_name},last name : {self.last_name}"


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"))
    city = Column(String())
    state = Column(String())
    postal_code = Column(String())

    user = relationship("User",back_populates="addresses",secondary=enrollments)

    def __repr__(self):
        return f"address(id:{self.id},state:{self.state},city:{self.city}"



"""
to create tables of the database
"""
Base.metadata.create_all(engine)


session = SessionLocal()

#-------------------INSERTING DATA----------------------
"""

kiarash = User(first_name="kiarash",age=20)
session.add(kiarash)
session.commit()

"""

#-------------------BULK INSERT(INSERT MULTIPLE ITEMS)----------------------
"""

ayeen = User(first_name= "ayeen", age=19)
shadkam = User(first_name= "shadkam", age=20)
arsalan = User(first_name= "arsalan", age=19)
users = [
    ayeen,
    shadkam,
    arsalan
]
session.add_all(users)
session.commit()

"""

#-------------------RETRIEVE DATA----------------------
"""
user_test = session.query(User).filter_by(first_name="kiarash").one_or_none()
user_test.last_name = "alimohamadi"
session.commit()
"""

#-------------------ADVANCED RETRIEVE DATA----------------------
"""
from sqlalchemy import or_,and_,not_,func
users = session.query(User).filter(User.age >= 19).all()
print(users)
#----> you can use "where" instead of "filter"

users2 = session.query(User).filter(or_(User.age >=19 , User.first_name=="kiarash")).all()

total_users = session.query(func.count(User.id)).scalar()
#-----> "scalar" returns a numeric response

max_age = session.query(func.max(User.age)).scalar()
"""

user = session.query(User).filter(User.id==1).one_or_none()
address = session.query(Address).filter(Address.state=="tehran").one_or_none()


print(user)
print(address)
#addresses = [Address(user_id = user.id,city="tehran",state="tehran",postal_code="1234567890"),
#            Address(user_id = user.id,city="isfahan",state="isfahan",postal_code="0004567000")]

#session.add_all(addresses)
#session.commit()


#addresses = session.query(Address).filter_by(user_id=user.id).all()
#print(addresses)


address.user.append(user)
session.commit()
