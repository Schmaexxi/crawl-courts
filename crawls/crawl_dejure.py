from crawl_util import nap, save_json, get_soup
import json
import atexit

with open("../data/judgements_dejure_olg_karlsruhe.json", "r") as f:
    data = json.load(f)

dest_file: str = "../data/judgements_dejure_olg_karlsruhe.json"


judgements: json = {}
if data:
    judgements = data

not_working_links = []
judgements['not_working_links'] = not_working_links

specific_url_prefix = 'https://www.dejure.org'

# register functions to execute when program terminates
atexit.register(save_json, data=judgements, file_name=dest_file)


# iteratively request url for judgements by year:
looped = False
for page in range(63, 1000):
    print(f"Current page: {page}")
    judgements['page'] = page
    if looped:
        break
    url: str = f"https://dejure.org/dienste/rechtsprechung?gericht=OLG%20Karlsruhe&seite={page}"
    soup = get_soup(url)
    if soup:
        container = soup.find('div', {'id': "alpha"})
        judgement_list = container.find('ul', {'class': "urteilsliste"})
        rows = judgement_list.find_all("li")
        if rows:
            for row in rows:
                nap(1)
                specific_url = specific_url_prefix + row.find("a")['href']
                specific_soup = get_soup(specific_url)
                if specific_soup:
                    case_data = specific_soup.find("td", {"class": "urteilszeile"})
                    if case_data:
                        comma_index = case_data.text.find(",")
                        hyphen_index = case_data.text.find("-")
                        date = case_data.text[comma_index+1: hyphen_index].split()[0]
                        file_number = case_data.text[hyphen_index+1:]
                        if file_number[0] == " ":
                            file_number = file_number[1:]
                        judgements[file_number] = date
                    else:
                        not_working_links.append(specific_url)
                        print(f"{specific_url} has no case data")
        else:
            looped = True

        nap(1)
        save_json(judgements, dest_file)
save_json(judgements, dest_file)
