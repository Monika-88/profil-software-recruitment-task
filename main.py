import json
from datetime import datetime, date
from pathlib import Path


def years_to_leap_year(year):
    def _is_leap(year):
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    year2 = year
    while True:
        year2 += 1
        if _is_leap(year2):
            return year2 - year


def get_days_to_birthday(person):
    current_date = datetime.utcnow()
    birthday_string = person.get('dob').get('date')
    birthday = datetime.strptime(birthday_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    try:
        if ((current_date.month, current_date.day) < (birthday.month, birthday.day)):
            days_to_birthday = date(current_date.year, birthday.month, birthday.day) - date(current_date.year, current_date.month, current_date.day)
        else:
            days_to_birthday = date(current_date.year + 1, birthday.month, birthday.day) - date(current_date.year, current_date.month, current_date.day)
    except ValueError:
        days_to_birthday = date(current_date.year + years_to_leap_year(current_date.year), birthday.month, birthday.day) - date(current_date.year, current_date.month, current_date.day)
    return days_to_birthday.days


def drop_phone_special_chars(person):
    phone = person['phone']
    digit_list = [char for char in phone if char.isnumeric()]
    return "".join(digit_list)


def drop_picture(person):
    try:
        del(person['picture'])
    except KeyError:
        pass


# Get relative path
main_path = Path(__file__).parent
# Add file name to main_path
file_path = main_path / "persons.json"

# Open file as f using file_path
with open(file_path, encoding='utf-8') as f:
    # save data from json file to
    json_data = json.load(f)

# get list of people NOT persons :)

people = json_data.get('results')
for person in people:
    person['dtb'] = get_days_to_birthday(person)
    person['phone'] = drop_phone_special_chars(person)
    drop_picture(person)

print(people[0])