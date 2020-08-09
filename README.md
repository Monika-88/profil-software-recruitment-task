# profil-software-recruitment-task
*Solution for Profil Software recruitment task.*

## How to use:
- Clone this repository.
- Database will be created from json file on first run.
- Run script.py -h for more info.
### Use examples:
usage: script.py [-h] [-g GENDER_PERCENTAGE] [-a AVERAGE_AGE] [-c MOST_POPULAR_CITIES] [-p MOST_POPULAR_PASSWORDS] [-b] [-b1 BORN_AFTER] [-b2 BORN_BEFORE] [-s]
- --help  (show this help message and exit)
- --gender_percentage <male/female> (displays percentage of given gender)
- --average_age <male/female/all> (displays average age for male, famale or all gender)
- --most_popular_cities <N> (displays a selected number of the most popular cities)
- --most_popular_passwords <N> (displays a selected number of the most popular passwords)
- --people_born_between (displays people born in the selected date range)
    - --born_after (date in format <YYYY-MM-DD>)
    - --born_before (date in format <YYYY-MM-DD>)
- --the_most_secure_password (displays the most secure password)





## Main tasks:  

- [x] loading data from persons.json file
- [x] processing data with given requirements 
- [x] saving data to database
    - [x] learn sqlalchemy basics
    - [x] test new learned skills
    - [x] implement fully functional saving to database algorithm
- [x] reading and processing data from database
- [x] displaying data in the right way (with the given reqs) 

### Side tasks: 
*(required but there is no need to make tasks chronologically)*

- [x] command line interface 
    - [x] learn argparse basics 
    - [x] test gathered knowledge in exercise task
    - [x] implement fully functional CLI with given reqs


### Bonus tasks:

- [ ] Loading data from https://randomuser.me/ API
- [ ] Pytest unit tests
