from telnetlib import SE
import requests
import os
import openai
from decouple import config
from bs4 import BeautifulSoup

url = "https://www.skillshot.pl/jobs/31190-grafik-generalista-at-jutsu-games-gameops"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

offer = soup.find("div", {"id": "job_presentation"})


class Parser:
    def __init__(self, soup):
        self.soup = soup
        self.job_presentation = soup.find("div", {"id": "job_presentation"})
        self.job_presentation_text = self.job_presentation.getText()

    def get_title(self):
        return self.job_presentation.find("h1").getText()

    def get_company(self):
        return self.job_presentation.find("b").getText()

    def get_location(self):
        return self.job_presentation.find_all("b")[1].getText()

    def get_category(self):
        return self.job_presentation.find(
            "span", {"class": "badge badge-default badge-job-category"}
        ).getText()

    def get_job_type(self):
        return (
            self.job_presentation.find(
                "span", {"class": "badge badge-default badge-job-category"}
            )
            .find_previous()
            .getText()
        )

    def get_date(self):
        return (
            self.job_presentation.find(
                string=lambda text: "data" in text.lower(), recursive=True
            )
            .find_next()
            .getText()
        )

    def get_views(self):
        return (
            self.job_presentation.find(
                string=lambda text: "liczba" in text.lower(), recursive=True
            )
            .find_next()
            .getText()
        )


class ParserGPT(Parser):
    pass

    def __init__(self, soup):
        super().__init__(soup)
        self.response = ""

    def get_prompt(self):
        return (
            "Extract the important entities mentioned in the text below. First extract is job remote, provide yes or no answer only. Then extract job seniority, then extract required technology. Finally extract salary, provide numbers only. \n"
            + "Desired format: \n"
            + " Is job remote \n"
            + " Seniority \n"
            + " Technology comma separated \n"
            + " Salary \n"
            + f" \nText: ### \n {self.job_presentation_text} \n ###"
        )

    def send_request(self):
        openai.api_key = config("OPENAI_API_KEY")
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt="Say this is a test",
            temperature=0,
        )
        self.response = completion.choices[0].message
        return self.response


xd = ParserGPT(soup)
print(xd.get_prompt())


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
