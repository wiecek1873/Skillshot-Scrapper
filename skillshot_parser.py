import re
import openai
from decouple import config


class Parser:
    def __init__(self, soup):
        self.soup = soup
        self.job_presentation = soup.find("div", {"id": "job_presentation"})

        if self.job_presentation != None:
            self.job_presentation_text = self.job_presentation.getText()

    def is_valid(self):
        return self.job_presentation != None

    def get_title(self):
        return self.job_presentation.find("h1").getText().lower()

    def get_company(self):
        return self.job_presentation.find("b").getText().lower()

    def get_location(self):
        return self.job_presentation.find('p').text.split(" w ",1)[1].split("\n")[0].lower()

    def get_category(self):
        return self.job_presentation.find(
            "span", {"class": "badge badge-default badge-job-category"}
        ).getText().lower()

    def get_job_type(self):
        return (
            self.job_presentation.find(
                "span", {"class": "badge badge-default badge-job-category"}
            )
            .find_previous()
            .getText()
            .lower()
        )

    def get_date(self):
        return (
            self.job_presentation.find(
                string=lambda text: "data publikacji:" in text.lower(), recursive=True
            )
            .find_next()
            .getText()
            .lower()
        )

    def get_views(self):
        return (
            self.job_presentation.find(
                string=lambda text: "liczba wy" in text.lower(), recursive=True
            )
            .find_next()
            .getText()
            .lower()
        )


class ParserGPT(Parser):
    pass

    def __init__(self, soup):
        super().__init__(soup)
        self.content = ""

    def get_prompt(self):
        return (
            'Extract the important entities mentioned in the text below. First extract is job fully remote, provide "yes", "no", "not specified" answer only. Then extract job seniority, provide "intern", "junior", "mid", "senior", "lead", "not specified" answers only. Then extract minimum salary like in example "5000". Then extract maximum salary like in example "10000". \n'
            + "Desired format: \n"
            + "Fully remote: \n"
            + "Seniority: \n"
            + "Minimum salary: \n"
            + "Maximum salary: \n"
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

    def get_seniority(self):
        self.try_initialize()
        return re.search(r"Seniority: (.*)", self.content).group(1).lower()

    def get_salary_min(self):
        self.try_initialize()
        return re.search(r"Minimum salary: (.*)", self.content).group(1).lower()

    def get_salary_max(self):
        self.try_initialize()
        return re.search(r"Maximum salary: (.*)", self.content).group(1).lower()
