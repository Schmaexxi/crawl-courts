from crawl_util import nap, save_json, get_soup, get_name_from_anchor_text
import json
import atexit


config = {"ignore_urls": ["youtube"]}
dest_file = "data/courts.json"

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
atexit.register(save_json, data=courts_by_state, file_name=dest_file)

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

            save_json(courts_by_state, dest_file)
