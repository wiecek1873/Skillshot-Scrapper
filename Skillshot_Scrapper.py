import requests
from bs4 import BeautifulSoup

url = "https://www.skillshot.pl/jobs/31190-grafik-generalista-at-jutsu-games-gameops"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

#offer = soup.find("div", {"id": "job_presentation"})


class Parser:
    def __init__(self, soup):
        self.soup = soup

    def get_job_presentation(cls):
        return cls.soup.find("div", {"id": "job_presentation"})


xd = Parser(soup)

print(xd.get_job_presentation())

class JobOffer:
    def __init__(
        self,
        title,
        company,
        location,
        remote,
        category,
        job_type,
        seniority,
        requirements,
        salary,
        date,
        views,
    ):
        self.title = title
        self.company = company
        self.location = location
        self.remote = remote
        self.category = category
        self.job_type = job_type
        self.seniority = seniority
        self.requirements = requirements
        self.salary = salary
        self.date = date
        self.views = views
