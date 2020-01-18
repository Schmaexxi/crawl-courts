import json
import re

with open("courts.json", 'r') as f:
    data = json.load(f)

"""
# remove all entries for courts labeled "Gerichte" or contain "gerichtsbarkeit"
for i in data['states']:
    for court in list(i['courts']):
        key = next(iter(court.keys()))
        if key == 'Gerichte' or 'gerichtsbarkeit' in key.lower() or key.lower().startswith('http'):
            i['courts'].remove(court)
"""
court_count = 0
court_count_with_website = 0

dejure_counter, juris_counter = 0, 0

courts_without_dejure = {}

court_names = set()

t = True
for i in data['states']:
    court_count += len(i['courts'])
    for court in i['courts']:
        if len(court[next(iter(court))]) > 0:
            court_count_with_website += 1
            # count number of courts with an outlink to dejure
            dejure_url = False
            key = next(iter(court))
            court_names.add(key)
            for url in court[key]:
                dejure_match = re.search("https://dejure", url)
                if dejure_match:
                    dejure_counter += 1
                    dejure_url = True
                juris_match = re.search("juris.", url)
                if juris_match:
                    juris_counter += 1

            if not dejure_url:
                courts_without_dejure[next(iter(court))] = court[next(iter(court))]

print("Courts with urls: ", court_count_with_website)
print("Courts without urls: ", court_count)


# get the number of courts that have no link to dejure
print("Courts with outlinks to dejure: ", dejure_counter)

with open("courts_without_dejure_outlinks.json", "w+") as f:
    json.dump(courts_without_dejure, f, indent=4)


with open("open_legal_data_courts.json", "r") as f:
    data = json.load(f)


print(len(data['courts']))

print(list(set(data['courts']).symmetric_difference(court_names)))

print(list(set(data['courts']) - court_names))
# names are not precise in either data source -
# USE GIT you idiot!!!!!!!
print(list(court_names - set(data['courts'])))
