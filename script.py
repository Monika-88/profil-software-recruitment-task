# -*- coding: utf-8 -*-
import argparse
from people_utils import get_people
from database import create_tables, add_data_to_database, get_gender_percentage, get_avg_age, get_most_popular_cities,\
                     get_most_popular_passwords, get_people_born_between_dates, most_secure_password
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == '__main__':
    SQLALCHEMY_DATABASE_URL = "sqlite:///people.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # create a Session
    session = Session()

    # get relative path
    main_path = Path(__file__).parent
    # add file name to main_path
    file_path = main_path / "people.db"
    # create database if not already created
    if not file_path.is_file():
        create_tables(engine)
        people = get_people()
        add_data_to_database(session, people)

    parser = argparse.ArgumentParser(
        description="Profil software recruitment task script. Choose option to display data."
    )
    parser.add_argument('-g', '--gender_percentage', type=str, help="<male/female> (displays percentage of given gender)")
    parser.add_argument('-a', '--average_age', type=str, help="<male/female/all> (displays average age for male, famale or all gender)")
    parser.add_argument('-c', '--most_popular_cities', type=str, help="<N> (displays a selected number of the most popular cities)")
    parser.add_argument('-p', '--most_popular_passwords', type=str, help="<N> (displays a selected number of the most popular passwords)")
    parser.add_argument('-b', '--people_born_between', action='store_true', help="displays people born in the selected date range")
    parser.add_argument('-b1', '--born_after', type=str, help="date in format <YYYY-MM-DD>")
    parser.add_argument('-b2', '--born_before', type=str, help="date in format <YYYY-MM-DD>")
    parser.add_argument('-s', '--the_most_secure_password', action='store_true', help="displays the most secure password")
    args = parser.parse_args()

    if args.gender_percentage:
        gender_percent = get_gender_percentage(session, args.gender_percentage)
        print(gender_percent)
    elif args.average_age:
        avg_age = get_avg_age(session, args.average_age)
        print(avg_age)
    elif args.most_popular_cities:
        cities = get_most_popular_cities(session, args.most_popular_cities)
        for city in cities:
            print("{}, {}".format(city[0], city[1]))
    elif args.most_popular_passwords:
        passwords = get_most_popular_passwords(session, args.most_popular_passwords)
        for password in passwords:
            print("{}, {}".format(password[0], password[1]))
    elif args.people_born_between:
        if args.born_after:
            if args.born_before:
                people = get_people_born_between_dates(session, args.born_after, args.born_before)
                for person in people:
                    print(person.name_first, person.name_last)
            else:
                raise Exception("Please provide date before person was born.")
        else:
            raise Exception("Please provide date after person was born.")
    elif args.the_most_secure_password:
        password = most_secure_password(session)
        print(password)
    else:
        print("Please try again")
