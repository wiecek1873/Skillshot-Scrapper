from typing import final
import requests
from bs4 import BeautifulSoup
from skillshot_parser import ParserGPT
from skillshot_parser import Parser
from job_offer import JobOffer
from serializer import serialize


def get_soup(url):
    response = requests.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        pass


def get_job_offer(url):
    soup = get_soup(url)
    if soup != None:
        parser = ParserGPT(soup)

        if(parser.is_valid()):
            return JobOffer(
                parser.get_title(),
                parser.get_company(),
                parser.get_location(),
                parser.get_remote(),
                parser.get_category(),
                parser.get_job_type(),
                parser.get_seniority(),
                parser.get_salary(),
                parser.get_date(),
                parser.get_views(),
                url
        )
        else:
            return None
    else:
        return None


base_url = "https://www.skillshot.pl/jobs/"

xd = Parser(get_soup(base_url + "31000"))
print(xd.get_views())
#print(get_job_offer(base_url + "31000").__dict__)

#while True:
#    from_string = input("Please enter starting offer index: ")
#    if from_string.isdigit():
#        break
#    else:
#        print("Invalid input. Please enter a positive number.")

#while True:
#    count_string = input("Please enter count: ")
#    if count_string.isdigit():
#        break
#    else:
#        print("Invalid input. Please enter a positive number.")

#index_start = int(from_string)
#index_count = int(count_string)

#offers = []

#try:
#    for index in range(index_start, index_start + index_count):
#        url = base_url + str(index)
#        print(f"Parsing offer with url {url}")
#        offers.append(get_job_offer(url))
#finally:
#    print("Saving...")
#    serialize("job_offers.csv", offers)
