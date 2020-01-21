from json import dump, dumps, loads, JSONEncoder, JSONDecoder
from crawl_util import get_file_len


f_name = "/Users/maximilianlangknecht/Downloads/cases.json"
court_output_name = "data/open_legal_data_courts.json"
print(get_file_len(f_name)) # 106325

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

# with open("data/open_legal_data_file_numbers_and_courts.json", "w+") as f:
#      dump(file_numbers, f, indent=4, ensure_ascii=False)

data = {"courts": list(courts)}
with open(court_output_name, "w+") as f:
    dump(data, f, indent=4, ensure_ascii=False)
