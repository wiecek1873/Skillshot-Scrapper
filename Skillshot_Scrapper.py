import requests
from bs4 import BeautifulSoup

url = "https://www.skillshot.pl/jobs/31190-grafik-generalista-at-jutsu-games-gameops"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

offer = soup.find("div", {"id": "job_presentation"})

class Parser:
    def __init__(self, soup):
        self.soup = soup
        self.job_presentation = soup.find("div", {"id": "job_presentation"})

    def get_title(cls):
        return cls.job_presentation.find("h1").getText()

    def get_company(cls):
        return cls.job_presentation.find("b").getText()

    def get_location(cls):
        return cls.job_presentation.find_all("b")[1].getText()

    #def get_is_remote(cls):
    #    return cls.soup.find(string="zdalnie")

    def get_category(cls):
        return cls.job_presentation.find("span", {"class": "badge badge-default badge-job-category"}).getText()

    def get_job_type(cls):
        return cls.job_presentation.find("span", {"class": "badge badge-default badge-job-category"}).find_previous().getText()

    def get_date(cls):
        return cls.job_presentation.las

xd = Parser(soup)

print(xd.get_title())


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
        technology,
        years_of_experience,
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
        self.technology = technology
        self.years_of_experience = years_of_experience
        self.salary = salary
        self.date = date
        self.views = views
