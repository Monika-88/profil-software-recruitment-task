from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///people.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

Base = declarative_base()

class PeopleTable(Base):
    __tablename__ = "people"
    idx = Column(Integer, primary_key=True, autoincrement=True)
    cell = Column(String)
    # dob = Column(DateTime)
    dtb = Column(Integer)
    # email = Column(String)
    # gender = Column(Boolean)
    # id_name = Column(String)
    # id_value = Column(String)
    # location = relationship("LocationTable", uselist=False, back_populates="people")
    # login = relationship("LoginTable", uselist=False, back_populates="people")
    # name_first = Column(String)
    # name_last = Column(String)
    # name_title = Column(String)
    # nat = Column(String)
    # phone = Column(String)
    # registered = Column(DateTime)

class LocationTable(Base):
    __tablename__ = "locations"
    location_idx = Column(Integer, primary_key=True, autoincrement=True)
#     people_idx = Column(Integer, ForeignKey('people.idx'))
#     people = relationship("PeopleTable", back_populates="locations")
#     city = Column(String)
#     latitude = Column(Float)
#     longitude = Column(Float)
#     country = Column(String)
#     postcode = Column(Integer)
#     state = Column(String)
#     street_name = Column(String)
#     street_number = Column(Integer)
#     timezone_description = Column(String)
#     timezone_offset = Column(String)

class LoginTable(Base):
    __tablename__ = "logins"
    login_idx = Column(Integer, primary_key=True, autoincrement=True)
#     people_idx = Column(Integer, ForeignKey('people.idx'))
#     people = relationship("PeopleTable", back_populates="logins")
#     md5 = Column(String)
#     password = Column(String)
#     salt = Column(String)
#     sha1 = Column(String)
#     sha256 = Column(String)
#     username = Column(String)
#     uuid = Column(String)


def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)

# create_tables()
