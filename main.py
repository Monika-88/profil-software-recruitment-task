import json
from pathlib import Path

# Get relative path
main_path = Path(__file__).parent
# Add file name to main_path
file_path = main_path / "persons.json"
# Open file as f using file_path
with open(file_path, encoding='utf-8') as f:
# save data from json file and get list of people NOT persons :)
    json_data = json.load(f)
people = json_data.get('results')
print(people[0])