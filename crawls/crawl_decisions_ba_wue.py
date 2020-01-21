from crawl_util import nap, save_json, get_soup
import json
import datetime
import atexit


dest_file: str = "../data/judgements_ba_wue.json"

start_year: int = 2000
this_year: int = datetime.datetime.now().year

max_page = 0

judgements: json = {}

# register functions to execute when program terminates
atexit.register(save_json, data=judgements, file_name=dest_file)


# iteratively request url for judgements by year
for year in range(start_year, this_year+1):
    looped = False
    for page in range(0, 500):
        if looped:
            break
        url: str = f"http://lrbw.juris.de/cgi-bin/laender_rechtsprechung/list.py?Gericht=bw&Art=en&Datum={year}&Seite={page}"
        soup = get_soup(url)

        container = soup.find('div', {'id': "inhalta"})
        table = container.findChild("form").findChild("table")
        potential_body = container.findChild("form").findChild("table").find("tbody")
        if potential_body:
            table = potential_body
        table = container.findChild("form").findChild("table")

        new_page = True

        if table is not None:
            # iterate table rows
            for row in table.find_all('tr'):
                court = row.find("td", {"class", "EGericht"})
                # skip if row has no court information
                if not court:
                    continue
                file_number = row.find("td", {"class", "EAz"}).get_text()
                # '&nbsp' in extracted string displayed as hex code '\xa0' -> encode to ascii and replace substituted indexes
                # this requires the string to be void of any question mark characters, as they will be replaced
                file_number = file_number.encode("ascii", "replace").decode("utf-8").replace("?", " ")
                # file_number already exists - > new year
                if judgements.get(file_number) is not None:
                    looped = True
                    break
                # '&nbsp' in extracted string displayed as hex code '\xa0'
                # ignore here however, since value is not used as dict key
                court_name = court.get_text()
                dates = row.find_all("td", {"class", "EDatum"})
                decision_date = dates[0].get_text()
                provision_date = dates[1].get_text()
                meta_data = {"court": court_name,
                             "decision_date" : decision_date,
                             "provision_date": provision_date
                             }

                judgements[file_number] = meta_data
        else:
            print("Table not found")
        if page > max_page:
            max_page = page
        nap(2)
    print(f"Maximum number of pages for year {year}: {max_page}")
    save_json(judgements, dest_file)
