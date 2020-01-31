from datetime import datetime
import json


with open("../data/judgements_dejure_olg_karlsruhe.json", "r") as f:
    data = json.load(f)

for file_number, date in data['file_number'].items():
    if date.find(".") != -1:
        d = datetime.strptime(date, "%d.%m.%Y")
        if d.year < 2000:
            print(file_number, d)
