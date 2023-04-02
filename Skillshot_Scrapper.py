import requests
from bs4 import BeautifulSoup
from skillshot_parser import ParserGPT
from job_offer import JobOffer

url = "https://www.skillshot.pl/jobs/31220"
response = requests.get(url)

print(response.status_code)

# if response.status_code != 200:
# return

soup = BeautifulSoup(response.content, "html.parser")

offer = soup.find("div", {"id": "job_presentation"})


# xd = ParserGPT(soup)
# print(xd.get_prompt())