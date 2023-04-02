import re
import openai
import json
from decouple import config


class Parser:
    def __init__(self, soup):
        self.soup = soup
        self.job_presentation = soup.find("div", {"id": "job_presentation"})

        if self.job_presentation != None:
            self.job_presentation_text = self.job_presentation.getText()

    def get_title(self):
        return self.job_presentation.find("h1").getText()

    def get_company(self):
        return self.job_presentation.find("b").getText()

    def get_location(self):
        return self.job_presentation.find('p').text.split('w ')[1].strip()

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
        self.content = ""

    def get_prompt(self):
        return (
            'Extract the important entities mentioned in the text below. First extract is job fully remote, provide "yes", "no", "not specified" answer only. Then extract job seniority, provide "intern", "junior", "mid", "senior", "lead", "not specified" answers only. Then extract required technology comma separated. Then extract required years of experience. Finally extract salary, provide numbers only. \n'
            + "Desired format: \n"
            + "Fully remote: \n"
            + "Seniority: \n"
            + "Technology: <technology-comma-separated> \n"
            + "Experience: \n"
            + "Salary: \n"
            + f" \nText: ### \n {self.job_presentation_text} \n ###"
        )

    def send_request(self):
        openai.api_key = config("OPENAI_API_KEY")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role" : "user", "content" : self.get_prompt()}
            ],
            temperature=0,
        )
        
        self.content = completion.choices[0].message.content
        return self.content
     
    def try_initialize(self):
        if self.content == "":
            self.send_request()

    def get_remote(self):
        self.try_initialize()
        return re.search(r"Fully remote: (.*)", self.content).group(1)

    def get_seniority(self):
        self.try_initialize()
        return re.search(r"Seniority: (.*)", self.content).group(1)

    def get_technology(self):
        self.try_initialize()
        return re.search(r"Technology: (.*)", self.content).group(1)

    def get_years_of_experience(self):
        self.try_initialize()
        return re.search(r"Experience: (.*)", self.content).group(1)

    def get_salary(self):
        self.try_initialize()
        return re.search(r"Salary: (.*)", self.content).group(1)
