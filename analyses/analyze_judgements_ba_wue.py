import json
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


in_file = "../data/judgements_ba_wue.json"

with open(in_file, 'r') as f:
    ba_wue_files = json.load(f)

in_file = "../data/open_legal_data_file_numbers_and_courts.json"

with open(in_file, 'r') as f:
    open_legal_data_files = json.load(f)

file_numbers_not_in_old = set(ba_wue_files) - set(open_legal_data_files)
print(len(file_numbers_not_in_old))

all_courts = {}
for v in ba_wue_files.values():
    cur_court = v['court'].encode("ascii", "replace").decode("utf-8").replace("?", " ")
    court_type = cur_court.split()[0]
    if court_type in all_courts:
        all_courts[court_type] += 1
    else:
        all_courts[court_type] = 1
print(all_courts)

courts = {}
for i in file_numbers_not_in_old:
    cur_court = ba_wue_files[i]['court'].encode("ascii", "replace").decode("utf-8").replace("?", " ")
    court_type = cur_court.split()[0]
    if court_type in courts:
        courts[court_type] += 1
    else:
        courts[court_type] = 1
print(courts)

for court_type in all_courts:
    if courts.get(court_type):
        all_courts[court_type] -= courts.get(court_type)

print(all_courts)

all_courts = {k: v for k, v in sorted(all_courts.items(), key=lambda item: -item[1])}
courts = {k: v for k, v in sorted(courts.items(), key=lambda item: -item[1])}
p1 = plt.bar(range(len(all_courts)), list(all_courts.values()), width=0.35)
p2 = plt.bar(range(len(all_courts)), list(courts.values()), width=0.35,
             bottom=list(all_courts.values()))
#plt.bar(range(len(courts)), list(courts.values()), align='center')
plt.xticks(range(len(courts)), list(courts.keys()), rotation='vertical')
plt.tick_params(axis='x', which='major', labelsize=9)
plt.xlabel("Court type (abbreviated)")
plt.title("Number of judgements for specific court types in \nBaWue and their occurance in Openlegaldata")
plt.legend((p1[0], p2[0]), ('Judgements in OLD', 'Judgements not in OLD'))
plt.show()
