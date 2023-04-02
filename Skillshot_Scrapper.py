from typing import final
import requests
from bs4 import BeautifulSoup
from skillshot_parser import ParserGPT
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
        return JobOffer(
            parser.get_title(),
            parser.get_company(),
            parser.get_location(),
            parser.get_remote(),
            parser.get_category(),
            parser.get_job_type(),
            parser.get_seniority(),
            parser.get_technology(),
            parser.get_years_of_experience(),
            parser.get_salary(),
            parser.get_date(),
            parser.get_views(),
        )
    else:
        return None


base_url = "https://www.skillshot.pl/jobs/"

while True:
    from_string = input("Please enter starting offer index: ")
    if from_string.isdigit():
        break
    else:
        print("Invalid input. Please enter a positive number.")

while True:
    count_string = input("Please enter count: ")
    if count_string.isdigit():
        break
    else:
        print("Invalid input. Please enter a positive number.")

index_start = int(from_string)
index_count = int(count_string)

offers = []

try:
    for index in range(index_start, index_start + index_count):
        url = base_url + str(index)
        print(f"Parsing offer with url {url}")
        offers.append(get_job_offer(url))

except Exception as e:
    print("An error occurred:", e)
    print("Interrupt...")
finally:
    print("Saving...")
    serialize("job_offers.csv", offers)
