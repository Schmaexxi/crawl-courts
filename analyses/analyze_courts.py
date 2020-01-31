import json
import re
import matplotlib.pyplot as plt
from textwrap import wrap


def count_urls_from_wikipedia(in_file):
    with open(in_file, 'r') as f:
        data = json.load(f)

    court_count = 0
    court_count_with_website = 0

    dejure_counter, juris_counter = 0, 0

    courts_without_dejure = {}

    court_names = set()

    url_frequency_by_state = {}

    t = True
    for i in data['states']:
        current_state = i['state']
        url_frequency_by_state[current_state] = {}
        court_count += len(i['courts'])
        for court in i['courts']:
            if len(court[next(iter(court))]) > 0:
                court_count_with_website += 1
                # count number of courts with an outlink to dejure
                dejure_url = False
                key = next(iter(court))
                court_names.add(key)
                for url in court[key]:
                    cut_url = url[:url.find("?")]
                    if url_frequency_by_state[current_state].get(cut_url):
                        url_frequency_by_state[current_state][cut_url] += 1
                    else:
                        url_frequency_by_state[current_state][cut_url] = 1
                    dejure_match = re.search("https://dejure", url)
                    if dejure_match:
                        dejure_counter += 1
                        dejure_url = True
                    juris_match = re.search("juris.", url)
                    if juris_match:
                        juris_counter += 1

                if not dejure_url:
                    courts_without_dejure[next(iter(court))] = court[next(iter(court))]
    print(f"Courts with urls: {court_count}\nCourts without urls: {court_count_with_website}\n"
          f"Courts with outlinks to dejure: {courts_without_dejure}")
    return url_frequency_by_state, court_names


url_frequency_by_state, court_names = count_urls_from_wikipedia("data/courts.json")


in_file = "data/open_legal_data_courts.json"

with open(in_file, "r") as f:
    open_legal_data = json.load(f)


# print unique court names, i.e. those that only appear in either file
print(list(set(open_legal_data['courts']).symmetric_difference(court_names)))

# print those courts that are only in open legal data
print(list(set(open_legal_data['courts']) - court_names))
# print those courts that are only in lrbw
print(list(court_names - set(open_legal_data['courts'])))
# -> not useful: names are not precise in either data source


print(url_frequency_by_state)
for k, v in url_frequency_by_state.items():
    url_frequency_by_state[k] = {key: val for key, val in sorted(v.items(), key=lambda item: -item[1])[:5]}
    # print(k, url_frequency_by_state[k])
    labels = ['\n'.join(wrap(l, 30)) for l in url_frequency_by_state[k].keys()]
    plt.barh(range(len(url_frequency_by_state[k])), list(url_frequency_by_state[k].values()))
    plt.yticks(range(len(url_frequency_by_state[k])), labels, rotation='horizontal')
    plt.tick_params(axis='y', which='major', labelsize=8)
    #plt.xlabel("Court type (abbreviated)")
    plt.title(f"Number of links by most common url for \n{k}")
    #plt.legend((p1[0], p2[0]), ('Judgements in OLD', 'Judgements not in OLD'))
    plt.tight_layout()
    plt.savefig(f"plots/urls_{k}")
    plt.show()