from ast import parse
from contextlib import nullcontext
import requests
from bs4 import BeautifulSoup
from skillshot_parser import Parser
from skillshot_parser import ParserGPT
from job_offer import JobOffer

def get_soup(url):
    response = requests.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        pass

def get_job_offer(url):
    soup = get_soup(url)
    if soup != None:
        parser = Parser(soup)
        #return JobOffer(parser.get_title(), parser.get_company(), parser.get_location())


url = "https://www.skillshot.pl/jobs/31220"
offer = get_job_offer(url)

print(offer)

# xd = ParserGPT(soup)
# print(xd.get_prompt())