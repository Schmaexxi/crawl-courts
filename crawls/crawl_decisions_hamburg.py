from crawl_util import nap, save_json, get_soup, find_nth_occurance
import json
import datetime
import atexit


dest_file: str = "../data/judgements_hamburg.json"

start_year: int = 2000
this_year: int = datetime.datetime.now().year

max_page = 0

judgements: json = {}

# register functions to execute when program terminates
atexit.register(save_json, data=judgements, file_name=dest_file)

offset = 1
url: str = f"http://www.rechtsprechung-hamburg.de/jportal/portal/page/bsharprod.psml?form=bsIntExpertSearch&st=ent&sm=es&desc=text&query=&desc=norm&query=&desc=court&query=&desc=filenumber&query=&desc=date&query=date&dateFrom=&dateTo=&neuesuche=Suchen&st=ent&st=ent&psOfTl={offset}"
soup = get_soup(url)
num_results_text = soup.find('div', {'id': "inhalt"}).find('div', {'class': "bghigh"}).findAll('p')[1].text
max_num_results = int(num_results_text[num_results_text.find('von')+4:].strip())

while offset <= max_num_results:
    url: str = f"http://www.rechtsprechung-hamburg.de/jportal/portal/page/bsharprod.psml?form=bsIntExpertSearch&st=ent&sm=es&desc=text&query=&desc=norm&query=&desc=court&query=&desc=filenumber&query=&desc=date&query=date&dateFrom=&dateTo=&neuesuche=Suchen&st=ent&st=ent&psOfTl={offset}"
    soup = get_soup(url)
    offset += 20

    table = soup.find('div', {'id': "inhalt"}).find('div', {'class': "resultlistofsearch"}).findChild("table")

    if table is not None:
        # iterate table rows
        file_number = ""
        date = ""
        for row in table.find_all('tr'):
            tds = row.findAll("td")
            for index, data in enumerate(tds):
                if index == 0:  # date
                    date = data.text.strip()
                else:  # title with number
                    temp = data.text
                    idx_first_bar = temp.find('|')+1
                    idx_snd_bar = find_nth_occurance(temp, '|', 2)
                    file_number = temp[idx_first_bar:idx_snd_bar].lstrip().rstrip()
            judgements[file_number] = date
    else:
        print("Table not found")
    # print(judgements)
    print(f"Current offset: {offset}")
    nap(2)

save_json(judgements, dest_file)
