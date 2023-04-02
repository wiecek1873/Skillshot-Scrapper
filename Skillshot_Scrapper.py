from telnetlib import SE
import requests
import os
import openai
from decouple import config
from bs4 import BeautifulSoup
from skillshot_parser import ParserGPT

url = "https://www.skillshot.pl/jobs/31220"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

offer = soup.find("div", {"id": "job_presentation"})


xd = ParserGPT(soup)
print(xd.get_prompt())