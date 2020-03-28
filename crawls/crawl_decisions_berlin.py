from crawl_util import nap, save_json, get_soup, find_nth_occurance
import json
import datetime


a = "http://www.gerichtsentscheidungen.berlin-brandenburg.de/jportal/portal/page/sammlung.psml/bs/10/"
b = get_soup(a)
t = b.find('div', {'id': 'kaljahr'}).find('div', {'class': 'first'}).find('a')
print(t['href'])
pass
exit()
dest_file: str = "../data/judgements_berlin.json"

start_year: int = 2000
this_year: int = datetime.datetime.now().year

max_page = 0

judgements: json = {}

# register functions to execute when program terminates
#atexit.register(save_json, data=judgements, file_name=dest_file)

weird_affixes = ["sm", "t1", "tn", "ub", "uh", "uq", "v1", "v9", "vd", "vj", "vz", "w9", "wb", "wg", "w0", "wu", "ww", "wy", "x5", "xe", "xj"]
offset = 1
end_reached = False

for weird_affix in weird_affixes:

    if end_reached:
        continue
    url: str = f"http://gerichtsentscheidungen.berlin-brandenburg.de/jportal/portal/t/15{weird_affix}/bs/10/page/sammlung.psml/js_peid/Trefferliste/media-type/html?currentNavigationPosition={offset}"
    soup = get_soup(url)
    offset += 15

    rows = soup.find('table', {'id': "samtabletl"}).findAll('tr')

    if rows is not None:
        # iterate table rows
        file_number = ""
        date = ""
        for row in rows:
            tds = row.findAll("td")
            for index, data in enumerate(tds):
                if index == 1:  # date
                    date = data.find('span').text.strip()
                    print(date)
                elif index == 2:  # title with number
                    print(data.text)
                    continue
                    temp = data.text
                    idx_first_bar = temp.find('|')+1
                    idx_snd_bar = find_nth_occurance(temp, '|', 2)
                    file_number = temp[idx_first_bar:idx_snd_bar].lstrip().rstrip()
            judgements[file_number] = date
    else:
        end_reached = True
    # print(judgements)
    nap(2)

#save_json(judgements, dest_file)
