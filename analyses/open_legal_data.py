from json import dump, loads
from crawl_util import get_file_len
# line 7: use your own file path

# data from https://static.openlegaldata.io/dumps/de/
# from 21.10.2019
f_name = "/Users/maximilianlangknecht/Downloads/cases.json"  # use your own file path
court_output_name = "data/open_legal_data_courts.json"
print(get_file_len(f_name))  # 106325

judgements = []
courts = set()
file_numbers = {}

with open(f_name, "r+") as f:
    for idx, l in enumerate(f):
        line_dict = loads(l)
        if line_dict.get('content'):
            del line_dict['content']
        judgements.append(line_dict)
        courts.add(line_dict['court']['name'])
        # file_numbers[line_dict['file_number']] = line_dict['court']['name']

# save all judgements with their file number and respective court in a designated file
with open("data/open_legal_data_file_numbers_and_courts.json", "w+") as f:
    dump(file_numbers, f, indent=4, ensure_ascii=False)

# save distinct courts in a designated file
data = {"courts": list(courts)}
with open(court_output_name, "w+") as f:
    dump(data, f, indent=4, ensure_ascii=False)
