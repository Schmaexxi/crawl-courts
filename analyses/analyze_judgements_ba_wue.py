import json
import matplotlib.pyplot as plt
import copy
import os


in_file = "../data/judgements_ba_wue.json"

with open(in_file, 'r') as f:
    ba_wue_files = json.load(f)

in_file = "../data/open_legal_data_file_numbers_and_courts.json"

with open(in_file, 'r') as f:
    open_legal_data_files = json.load(f)

file_numbers_not_in_old = set(ba_wue_files) - set(open_legal_data_files)
print(len(file_numbers_not_in_old))

cases_olg_karlsruhe_ba_wue = set()

# dict of type of of courts and their count of occurrence
courts_ba_wue = {}
for k, v in ba_wue_files.items():
    # replace weird hex values in string with a white-space
    cur_court = v['court'].encode("ascii", "replace").decode("utf-8").replace("?", " ")
    if "OLG" in cur_court and "Karlsruhe" in cur_court:
        cases_olg_karlsruhe_ba_wue.add(k)

    court_type = cur_court.split()[0]
    if court_type in courts_ba_wue:
        courts_ba_wue[court_type] += 1
    else:
        courts_ba_wue[court_type] = 1
print("courts_ba_wue:", courts_ba_wue)

#
courts_not_in_old = {}
# count court type occurrence of file numbers not occurring in old
for i in file_numbers_not_in_old:
    # replace weird hex values in string with a white-space
    cur_court = ba_wue_files[i]['court'].encode("ascii", "replace").decode("utf-8").replace("?", " ")
    court_type = cur_court.split()[0]
    if court_type in courts_not_in_old:
        courts_not_in_old[court_type] += 1
    else:
        courts_not_in_old[court_type] = 1
print("courts_not_in_old:", courts_not_in_old)

courts_in_old = copy.deepcopy(courts_ba_wue)
for court_type in courts_in_old:
    if courts_not_in_old.get(court_type):
        courts_in_old[court_type] -= courts_not_in_old.get(court_type)

print("courts_in_old: ", courts_in_old)

# create ordered list to follow for both plots
sorted_court_names_and_counts = sorted(courts_ba_wue.items(), key=lambda item: -item[1])
# only use court name
sorted_court_names = [first_val for first_val, _ in sorted_court_names_and_counts]

courts_in = {}
courts_out = {}
for c in sorted_court_names:
    courts_in[c] = courts_in_old[c]
    courts_out[c] = courts_not_in_old[c]

fig, ax = plt.subplots()

courts_in_lst = list(courts_in.values())
courts_out_lst = list(courts_out.values())

p1 = ax.bar(range(len(courts_in_lst)), courts_in_lst, width=0.35)
p2 = ax.bar(range(len(courts_in_lst)), courts_out_lst, width=0.35,
            bottom=courts_in_lst)
ax.set_xticks(range(len(courts_out)))
ax.set_xticklabels(list(courts_out.keys()), rotation='vertical')
ax.tick_params(axis='x', which='major', labelsize=9, labelrotation=1)
ax.set_xlabel("Court type (abbreviated)")
ax.set_title("Number of judgements for specific court types in BaWue\n extracted from juris and their occurrence in Openlegaldata")
ax.legend((p1[0], p2[0]), ('Judgements in OLD', 'Judgements not in OLD'))
for i, v in enumerate(courts_out_lst):
    total_count = courts_in_lst[i] + v
    percent_out = round(v/total_count*100)
    percent_in = round(courts_in_lst[i]/total_count*100)
    ax.text(i + 0.16, total_count, "{}%".format(percent_out), color='orange', fontsize=8)
    ax.text(i + 0.16, 0, "{}%".format(percent_in), color='blue', fontsize=8)
fig.savefig("../plots/bawue_judgements_in_old")


print(cases_olg_karlsruhe_ba_wue)
with open("../data/judgements_dejure_olg_karlsruhe.json", "r") as f:
    dejure_data = json.load(f)

cases_olg_karlsruhe_dejure = set()
for key in dejure_data['file_number']:
    cases_olg_karlsruhe_dejure.add(key)

print(len(cases_olg_karlsruhe_ba_wue))
print(len(cases_olg_karlsruhe_ba_wue - cases_olg_karlsruhe_dejure))
print(len(cases_olg_karlsruhe_ba_wue - set(open_legal_data_files)))

cases_count_ba_wue = len(cases_olg_karlsruhe_ba_wue)
count_cases_out_dejure = len(cases_olg_karlsruhe_ba_wue - cases_olg_karlsruhe_dejure)
count_cases_in_dejure = cases_count_ba_wue - count_cases_out_dejure
print(cases_count_ba_wue, count_cases_out_dejure, count_cases_in_dejure)


count_cases_out_old = len(cases_olg_karlsruhe_ba_wue - set(open_legal_data_files))
count_cases_in_old = cases_count_ba_wue - count_cases_out_old

print(cases_count_ba_wue, count_cases_out_old, count_cases_in_old)

cases_in = [count_cases_in_dejure, count_cases_in_old]
cases_out = [count_cases_out_dejure, count_cases_out_old]
print(cases_in, cases_out)
fig1, ax1 = plt.subplots()

p1 = ax1.bar(range(len(cases_in)), cases_in, width=0.35)
p2 = ax1.bar(range(len(cases_in)), cases_out, width=0.35,
             bottom=cases_in)

ax1.set_xticks(range(len(cases_out)))
ax1.set_xticklabels(["Dejure", "Openlegaldata"], rotation='vertical')
ax1.tick_params(axis='x', which='major', labelsize=9, labelrotation=1)
ax1.set_xlabel("Sources")
ax1.set_title("Availability of judgements of the OLG Karlsruhe\nfrom juris in other sources")
ax1.legend((p1[0], p2[0]), ('Number of cases\navailable', 'Number of cases\nnot available'), loc="lower center")
for i, v in enumerate(cases_in):
    ax1.text(i+0.05, v-v/10, str(v), color='orange', fontweight='bold')
for i, v in enumerate(cases_out):
    ax1.text(i+0.085, cases_in[i] + v/10, str(v), color='blue', fontweight='bold')
fig1.savefig("../plots/dejure_vs_old")
plt.show()
