from datetime import datetime
from sqlalchemy import create_engine, event, desc, Boolean, Column, ForeignKey, Integer, String, DateTime, Float, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, load_only
from sqlalchemy.sql import func
from people_utils import get_people
import re

SQLALCHEMY_DATABASE_URL = "sqlite:///people.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


event.listen(engine, 'connect', _fk_pragma_on_connect)

# in memory database for testing
# engine = create_engine('sqlite://', echo=True)
# create a configured "Session" class
Session = sessionmaker(bind=engine)
# create a Session
session = Session()

Base = declarative_base()

class PeopleTable(Base):
    __tablename__ = "people_main"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    cell = Column(String)
    dob = Column(DateTime)
    dtb = Column(Integer)
    email = Column(String)
    gender = Column(String)
    id_name = Column(String)
    id_value = Column(String)
    locations = relationship("LocationTable", uselist=False, back_populates="people")
    logins = relationship("LoginTable", uselist=False, back_populates="people")
    name_first = Column(String)
    name_last = Column(String)
    name_title = Column(String)
    nat = Column(String)
    phone = Column(String)
    registered_date = Column(DateTime)
    registered_age = Column(Integer)


class LocationTable(Base):
    __tablename__ = "locations"

    location_idx = Column(Integer, primary_key=True, autoincrement=True)
    people_idx = Column(Integer, ForeignKey(PeopleTable.id, ondelete='cascade'))
    people = relationship(PeopleTable, back_populates="locations")
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String)
    postcode = Column(Integer)
    state = Column(String)
    street_name = Column(String)
    street_number = Column(Integer)
    timezone_description = Column(String)
    timezone_offset = Column(String)


class LoginTable(Base):
    __tablename__ = "logins"

    login_idx = Column(Integer, primary_key=True, autoincrement=True)
    people_idx = Column(Integer, ForeignKey(PeopleTable.id, ondelete='cascade'))
    people = relationship(PeopleTable, back_populates="logins")
    md5 = Column(String)
    password = Column(String)
    salt = Column(String)
    sha1 = Column(String)
    sha256 = Column(String)
    username = Column(String)
    uuid = Column(String)


def create_tables():
    Base.metadata.create_all(engine)


def get_date(string_date):
    return datetime.strptime(string_date, "%Y-%m-%dT%H:%M:%S.%fZ")

create_tables()
session.execute('pragma foreign_keys=on')
people = get_people()
for person in people:
    people = {'age': person['dob']['age'], 'cell': person['cell'], 'dob': get_date(person['dob']['date']),
            'dtb': person['dtb'], 'email': person['email'], 'gender': person['gender'], 'id_name': person['id']['name'],
            'id_value': person['id']['value'], 'name_first': person['name']['first'],
            'name_last': person['name']['last'], 'name_title': person['name']['title'], 'nat': person['nat'],
            'phone': person['phone'], 'registered_date': get_date(person['registered']['date']),
            'registered_age': person['registered']['age']}
    people_table = PeopleTable(**people)
    session.add(people_table)
    session.commit()
    loc = person['location']
    locations = {'people_idx': people_table.id, 'city': loc['city'], 'latitude': loc['coordinates']['latitude'],
                 'longitude': loc['coordinates']['longitude'], 'country': loc['country'], 'postcode': loc['postcode'],
                 'state': loc['state'], 'street_name': loc['street']['name'], 'street_number': loc['street']['number'],
                 'timezone_description': loc['timezone']['description'], 'timezone_offset': loc['timezone']['offset']}
    session.add(LocationTable(**locations))

    log = person['login']
    login = {'people_idx': people_table.id, 'md5': log['md5'], 'password': log['password'], 'salt': log['salt'], 'sha1': log['sha1'],
             'sha256': log['sha256'], 'username': log['username'], 'uuid': log['uuid']}
    session.add(LoginTable(**login))
    session.commit()


def get_gender_percentage(session, gender):
    male_num = session.query(PeopleTable).filter(PeopleTable.gender == "male").count()
    female_num = session.query(PeopleTable).filter(PeopleTable.gender == "female").count()
    # in case of other gender :)
    all_num = session.query(PeopleTable).count()
    if gender == 'male':
        return male_num / all_num * 100
    elif gender == 'female':
        return female_num / all_num * 100
    else:
        raise Exception("Gender {} not supported.".format(gender))


def get_avg_age(session, group):
    if group == 'all':
        avg = session.query(func.avg(PeopleTable.age)).all()[0]
    elif group == 'male':
        avg = session.query(func.avg(PeopleTable.age)).filter(PeopleTable.gender == "male").one()[0]
    elif group == 'female':
        avg = session.query(func.avg(PeopleTable.age)).filter(PeopleTable.gender == "female").one()[0]
    else:
        raise Exception("Group {} not supported.".format(group))
    return round(avg, 2)

def get_most_popular_cities(session, num):
    return session.query(LocationTable.city, func.count(LocationTable.city)).order_by(
                         desc(func.count(LocationTable.city))).group_by(LocationTable.city).limit(num).all()


def get_most_popular_passwords(session, num):
    return session.query(LoginTable.password, func.count(LoginTable.password)).order_by(
                         desc(func.count(LoginTable.password))).group_by(LoginTable.password).limit(num).all()


def get_users_born_between_dates(session, date1, date2):
    return session.query(PeopleTable).filter(PeopleTable.dob.between(date1, date2)).all()

def most_secure_password(session):
    all_passwd = session.query(LoginTable.password).group_by(LoginTable.password).all()
    best_score = 0
    best_passwd = ""
    for passwd in all_passwd:
        lower, upper, digit, eight_or_more, special_char = 0, 0, 0, 0, 0
        passwd = passwd[0]
        for i, char in enumerate(passwd):
            if char.islower():
                lower = 1
            elif char.isupper():
                upper = 2
            elif char.isdigit():
                digit = 1
            elif not re.match("^[a-zA-Z0-9_]*$", char):
                special_char = 3
            if i + 1 >= 8:
                eight_or_more = 5
        score = lower + upper + digit + eight_or_more + special_char
        if best_score < score:
            best_score = score
            best_passwd = passwd
    return best_passwd





