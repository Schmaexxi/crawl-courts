from crawl_util import nap, save_json, get_soup
import json
import atexit


def crawl_arbitrary_dejure(start_url: str, out_file: str, in_file="", start_page=1):
    """
    Crawls dejure.org for judgments of specific courts
    :param start_url: url to be crawled - example 'https://dejure.org/dienste/rechtsprechung?gericht=ArbG%20Hamburg'
    :param out_file: file to save
    :param in_file: if provided keeps adding judgements to an existing json file - useful for resuming a cancelled crawl
    :param start_page: get parameter 'seite' indicating at which page to start crawling
    :return: None
    """
    #  save content of in_file
    judgements: json = {}
    if in_file != "":
        with open(in_file, "r") as f:
            data = json.load(f)
        if data:
            judgements = data
            start_page = judgements['page']

    # register functions to execute when program terminates
    atexit.register(save_json, data=judgements, file_name=out_file)

    # iteratively request url for judgements by year:
    for page in range(start_page, 1000):
        print(f"Current page: {page}")
        judgements['page'] = page
        url: str = start_url + f"&seite={page}"
        soup = get_soup(url)
        if soup:
            container = soup.find('div', {'id': "alpha"})
            judgement_list = container.findAll('ul', {'class': "urteilsliste"})
            if len(judgement_list) == 1:  # normal case
                judgement_list = judgement_list[0]
            elif len(judgement_list) > 1:
                # first page view contains two unlinked lists with the required class - we choose the second list here
                judgement_list = judgement_list[1]
            else:  # this case has not occurred yet
                print(f"More than two lists found on page{page}, check that!")
            rows = judgement_list.find_all("li")  # get all judgements
            if rows:
                for row in rows:  # iterate judgements
                    file_name = row.find("a").text
                    comma_index = file_name.find(",")
                    hyphen_index = file_name.find("-")

                    # based on the structure of their files the following extraction of
                    # the date and file number may not always hold true
                    # we expect their comma and hyphen in the text to separate the date and file number
                    date = file_name[comma_index + 1: hyphen_index].split()[0]
                    file_number = file_name[hyphen_index + 1:].lstrip().rstrip()

                    judgements[file_number] = date
            else:
                # if no unlinked list with the class 'urteilsliste' is found the iteration will stop
                break

            nap(4)  # timeout between requests necessary to not get blokcked
            save_json(judgements, dest_file)
    save_json(judgements, dest_file)


# invoke function
link = "https://dejure.org/dienste/rechtsprechung?gericht=ArbG%20Hamburg"
dest_file: str = "../data/judgements_dejure_ag_hamburg.json"
crawl_arbitrary_dejure(link, dest_file, start_page=49)
