from json import dump, dumps, loads, JSONEncoder, JSONDecoder
import pickle


def file_len(f_name):
    with open(f_name, "r+") as f:
        for i, l in enumerate(f):
            pass
    return i + 1


f_name = "/Users/maximilianlangknecht/Downloads/cases.json"
court_output_name = "./open_legal_data_courts.json"
# print(file_len(f_name)) # 106325

judgements = []
courts = set()

with open(f_name, "r+") as f:
    for idx, l in enumerate(f):
        line_dict = loads(l)
        if line_dict.get('content'):
            del line_dict['content']
        judgements.append(line_dict)
        # print(idx/106325*100)
        courts.add(line_dict['court']['name'])
        # print(line_dict['court']['name'])
print(next(iter(judgements)))
print(courts)

data = {"courts": list(courts)}
with open(court_output_name, "w+") as f:
    dump(data, f, indent=4, ensure_ascii=False)
