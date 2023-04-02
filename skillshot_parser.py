import openai
from decouple import config


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
        return self.job_presentation.find('p').text.split('w ')[1]

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
        completion = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=self.get_prompt(),
            temperature=0,
        )
        self.response = completion.choices[0].message
        return self.response
