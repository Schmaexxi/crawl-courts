import requests
from bs4 import BeautifulSoup
from random import random
from time import sleep
import json
import atexit
from urllib.parse import unquote

config = {"ignore_urls": ["youtube"]}


def nap(duration: int = 2):
    """
    sleep for a duration roughly specified by the input parameter
    """
    sleep(random()*duration)


def save_to_file(content: str, dest_file: str):
    """
    Saves some object as text in a specified file (overwrites!)
    :param content: object to write
    :param dest_file: file to write to
    """
    with open(dest_file, "w") as f:
        f.write(str(content))


def get_soup(url_: str, parser: str = "lxml"):
    """
    starts an http GET-request and, if successful, returns its contents as a BeautifulSoup item
    :param url_: url to request
    :param parser: beautifulsoup parser
    :return: None or BeautifulSoup object
    """
    try:
        r = requests.get(url_)
    except requests.exceptions.ConnectionError as e:
        print(e)
        r = None
        pass

    if r is None:
        return r
    else:
        return BeautifulSoup(r.content, parser)


def save_json(data: json, file_name: str):
    """
    Save some json object in a json file
    :param data: json object
    :param file_name: file to write to
    """
    with open(file_name, "w+") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_name_from_anchor_text(court_link_):
    """
    looks for '/' in string trying to return its right-side text
    :return:
    """
    court_name_and_type = court_link.text
    right_most_slash_idx = court_link['href'].rfind('/')
    # if there is a slash in the link and the slash is not the last element of the link
    if right_most_slash_idx != -1 and right_most_slash_idx + 1 < len(court_link['href']):
        court_name_and_type = court_link['href'][court_link['href'].rfind('/'):]
        court_name_and_type = court_name_and_type.replace('/', '').replace('_', ' ')
        court_name_and_type = unquote(court_name_and_type)

    return court_name_and_type

# german site version!
url_prefix: str = "https://de.wikipedia.org"

url_suffix: str = "/wiki/Liste_deutscher_Gerichte"

url: str = url_prefix + url_suffix

soup = get_soup(url)

courts_by_state: json = {"states": [],
                         "courts_without_urls": []}

# collect all visited urls for states
visited_states_urls = []

allowed_urls= ["wiki/Liste_der_Gerichte", "/wiki/Bundesgericht_(Deutschland)"]

# register functions to execute when program terminates
atexit.register(save_json, data=courts_by_state, file_name='courts.json')

# iterate list of all anchor tags from wikipedia
for a in soup.find_all('a', href=True):
    
    # does link contain desired string that hints to link to a collection of courts by state?
    if any(x in a['href'] for x in allowed_urls) and a['href'] not in visited_states_urls:
        visited_states_urls.append(a['href'])
        print(visited_states_urls)
        # print("Next state that will be crawled: ", url_prefix + a.get('href'))
        supper = get_soup(url_prefix + a.get('href'))

        # initialize json for current state
        current_state = {"state": a.text, "courts": []}
        # add current state 
        courts_by_state['states'].append(current_state)

        # iterate all anchor tags - the soup object should list all courts for the specified state
        for court_link in supper.find_all('a', href=True):
            link_text = court_link.text.lower()
            url_text = court_link['href'].lower()
            # ignore false links to anchor tags of similar appaerance
            if ("gericht" in link_text and not link_text == "gerichte" and not "gerichtsbarkeit" in link_text and not link_text.startswith('http')) \
                    or ((any(x in url_text for x in['amtsgericht', 'arbeitsgericht', 'sozialgericht', 'verwaltungsgericht', 'finanzgericht', 'landgericht'])) and not "gerichtsbarkeit" in url_text):
                # print("Next court that will be crawled: ", url_prefix + court_link.get('href'))

                # get soup object for individual courts for the current state
                court = get_soup(url_prefix + court_link.get('href'))

                # if url was invalid
                if court is None:
                    # print("No connection could be established for: ", url_prefix + court_link.get('href'))
                    # print("Trying '", court_link.get('href'), "'instead!")
                    nap(1)
                    # wikipedia link structure is not consistent - sometimes relative sometimes absolute
                    court = get_soup(court_link.get('href'))
                    if court is None:
                        continue

                nap()
                # find "Weblink"-section
                web_link_span = court.find(id="Weblinks")
                if web_link_span is not None:
                    links: list = []
                    web_link_section = web_link_span.find_next('ul')

                    # search all links in the list of links
                    for endpoint in web_link_section.find_all('a', href=True):
                        link_text = endpoint.get('href')
                        # only use external links and ignore those specified by config file
                        if not link_text.startswith('/wiki') and not any(x in link_text for x in config['ignore_urls']):
                            links.append(link_text)

                    # get type and name of court from a-tag rather than text, as text is inconsistent
                    court_name_and_type = get_name_from_anchor_text(court_link)
                    current_state["courts"].append({court_name_and_type: links})
                    # print(current_state)
                # if no web links exist
                else:
                    courts_by_state['courts_without_urls'].append((court_link.text, court_link.get('href')))
                    # print(web_link_span)

            save_json(courts_by_state, "courts.json")
