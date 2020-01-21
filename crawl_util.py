import requests
from bs4 import BeautifulSoup
from random import random
from time import sleep
import json
from urllib.parse import unquote


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
    court_name_and_type = court_link_.text
    right_most_slash_idx = court_link_['href'].rfind('/')
    # if there is a slash in the link and the slash is not the last element of the link
    if right_most_slash_idx != -1 and right_most_slash_idx + 1 < len(court_link_['href']):
        court_name_and_type = court_link_['href'][court_link_['href'].rfind('/'):]
        court_name_and_type = court_name_and_type.replace('/', '').replace('_', ' ')
        court_name_and_type = unquote(court_name_and_type)

    return court_name_and_type


def get_file_len(f_name):
    with open(f_name, "r+") as f:
        for i, l in enumerate(f):
            pass
    return i + 1
